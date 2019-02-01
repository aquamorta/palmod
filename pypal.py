#!/usr/bin/env python
########################################################################
# Copyright (c) 2019 by bernd.  All Rights Reserved 
########################################################################
# pypal.py
# Author: bernd
#- 
# History:
#      b - Jan 30, 2019: Created.
########################################################################

import argparse
import re

class State(object):

    def __init__(self):
        self.relTo={'X':0,'Y':0,'Z':0,'E':0}
        self.state={'X':0,'Y':0,'Z':0,'E':0}
        self.lines=0
        self.absolute=True

    def count(self):
        self.lines+=1
    
    def move(self,axis,value):
        if self.absolute:
            self.state[axis]=value
        else:
            self.state[axis]=self.state.get(axis,0)+value

    def absPos(self,axis):
        return self.relTo.get(axis,0)+self.state.get(axis,0)
    
    def setPos(self,axis,value):
        self.relTo[axis]=self.absPos(axis)-value
        self.state[axis]=value


class Command(object):
    COMMENT_PRE=r'\s*;\s*'
    FLOAT_PAT=r'-?(\d+\.?\d*|\.\d+)'
    MOVE_PAT=r'(\s+([XYZEF])%s)'%FLOAT_PAT
    AXIS_PAT=r'(\s+[XYZE])?'

    def process(self,line,processor):
        return False

class CountCmd(Command):
    def process(self,line,processor):
        processor.state.count()
        return False


class MoveCmd(Command):
    PATTERN=re.compile(r'G0*[01]%s%s?%s?%s?%s?'%(Command.MOVE_PAT,Command.MOVE_PAT,Command.MOVE_PAT,Command.MOVE_PAT,Command.MOVE_PAT))

    def process(self,line,processor):
        m=self.PATTERN.match(line)
        pos=processor.state
        if m:
            i=2
            while i<len(m.groups()) and m.group(i):
                pos.move(m.group(i),float(m.group(i+1)))
                i+=3
        return m!=None    
        
class HomeCmd(Command):
    PATTERN=re.compile(r'G28%s%s%s%s'%(Command.AXIS_PAT,Command.AXIS_PAT,Command.AXIS_PAT,Command.AXIS_PAT))

    def process(self,line,processor):
        m=self.PATTERN.match(line)
        pos=processor.state
        if m:
            i=2
            while i<len(m.groups()) and m.group(i):
                pos.move(m.group(i),0)
                i+=1
        return m!=None    

class SetPosCmd(Command):
    PATTERN=re.compile(r'G92%s%s?%s?%s?'%(Command.MOVE_PAT,Command.MOVE_PAT,Command.MOVE_PAT,Command.MOVE_PAT))

    def process(self,line,processor):
        m=self.PATTERN.match(line)
        pos=processor.state
        if m:
            i=2
            while i<len(m.groups()) and m.group(i):
                pos.setPos(m.group(i),float(m.group(i+1)))
                i+=3
        return m!=None    

class ModifyCommand(Command):
    def process(self,line,processor):
        return line


class LookForChangeStart(ModifyCommand):
    COLOR_CHANGE=re.compile(r'^%stoolchange'%Command.COMMENT_PRE)

    def process(self,line,processor):
        if self.COLOR_CHANGE.match(line):
            processor.setMode(processor.CHANGE)
        return line

class LookForChangeEnd(ModifyCommand):
    COLOR_CHANGE_END=re.compile(r'^%sendchroma'%Command.COMMENT_PRE)

    def process(self,line,processor):
        if self.COLOR_CHANGE_END.match(line):
            processor.setMode(processor.DEFAULT)
        return line

            
class ChangeSpeed(ModifyCommand):
    EXTRUDER_PAT=re.compile(r'^(G0?1\s+E%s)\s+F2400\s+'%Command.FLOAT_PAT)
    EXTRUDER_REP='%s F200\r\n'

    def process(self,line,processor):
        m=self.EXTRUDER_PAT.match(line)
        if m:
            nline=self.EXTRUDER_REP%m.group(1)
            print 'line [%d] changing "%s" --> "%s"'%(processor.state.lines,line.strip(),nline.strip())
            line=nline
        return line
    

class Processor(object):
    DEFAULT='D'
    CHANGE='C'

    GENERAL_TABLE=[CountCmd(),MoveCmd(),HomeCmd(),SetPosCmd()]
    MODE_TABLE={DEFAULT:[LookForChangeStart()],CHANGE:[ChangeSpeed(),LookForChangeEnd()]}
    
    def __init__(self,args):
        self.args=args
        self.state=State()
        self.mode=Processor.DEFAULT

    def setMode(self,mode):
        self.mode=mode
        
    def process(self):
        with open(args.output,'w') as ofd:
            with open(self.args.input,'r') as fd:
                for line in fd.readlines():
                    for cmd in self.GENERAL_TABLE:
                        if cmd.process(line,self):
                            break
                    for cmd in self.MODE_TABLE.get(self.mode,[]):
                        line=cmd.process(line,self)
                    ofd.write(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='processing a palette gcode file')
    parser.add_argument('-i', '--input',help='input file ',required=True)
    parser.add_argument('-o', '--output',help='output file ',required=True)

    args = parser.parse_args()
    proc=Processor(args)
    proc.process()


