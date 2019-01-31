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

class Position(object):

    def __init__(self):
        self.relTo={'X':0,'Y':0,'Z':0,'E':0}
        self.pos={'X':0,'Y':0,'Z':0,'E':0}
        self.absolute=True

    def move(self,axis,value):
        if self.absolute:
            self.pos[axis]=value
        else:
            self.pos[axis]=self.pos.get(axis,0)+value
    
    def setRef(self,axis,value): 
        pass
    

class Processor(object):
    COMMENT_PRE=r'\s*;\s*'
    INT_PAT = r'*-?\d+'
    FLOAT_PAT=r'-?(\d+\.?\d*|\.\d+)'
    COLOR_CHANGE=re.compile(r'^%stoolchange'%COMMENT_PRE)
    COLOR_CHANGE_END=re.compile(r'^%sendchroma'%COMMENT_PRE)
    EXTRUDER_PAT=re.compile(r'^(G0?1\s+E%s)\s+F2400\s+'%FLOAT_PAT)
    EXTRUDER_REP='%s F200\r\n'
    MOVE_PAT=r'(\s+([XYZEF])%s)'%FLOAT_PAT

    POS_CMD=re.compile(r'G0*[01]%s%s?%s?%s?%s?'%(MOVE_PAT,MOVE_PAT,MOVE_PAT,MOVE_PAT,MOVE_PAT))

    DEFAULT='D'
    PROCESS='C'
    

    FSM={
        (DEFAULT,POS_CMD):Processor.
        'CHANGE'
        }


    def __init__(self,args):
        self.args=args
        self.func=self._scan
        self.lineNo=0
        self.pos=Position()
        
    def _scan(self,line):
        self.ofd.write(line)
        if self.COLOR_CHANGE.match(line):
            self.func=self._search

    def _search(self,line):
        m=self.EXTRUDER_PAT.match(line)
        if m:
            nline=self.EXTRUDER_REP%m.group(1)
            print 'line [%d] changing "%s" --> "%s"'%(self.lineNo,line.strip(),nline.strip())
            self.ofd.write(self.EXTRUDER_REP%m.group(1))
        else:
            self.ofd.write(line)
            if self.COLOR_CHANGE_END.match(line):
                self.func=self._scan

    def move(self,matches):
        i=1
        while i<len(matches) and matches.group(i):
            self.pos.move(matches.group(i),matches.group(i+1))
            i+=3

    def home(self,matches):
        pass
    
    def process(self):
        with open(args.output,'w') as self.ofd:
            with open(self.args.input,'r') as fd:
                for line in fd.readlines():
                    self.lineNo+=1
                    m=self.POS_CMD.match(line)
                    if m:
                       self.move(m) 
                    self.func(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='processing a palette gcode file')
    parser.add_argument('-i', '--input',help='input file ',required=True)
    parser.add_argument('-o', '--output',help='output file ',required=True)

    args = parser.parse_args()
    proc=Processor(args)
    proc.process()


