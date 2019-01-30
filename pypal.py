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

class Processor(object):
    COMMENT_PRE=r'\s*;\s*'
    INT_PATTERN = r'*-?\d+'
    FLOAT_PATTERN=r'-?(\d+\.?\d*|\.\d+)'
    COLOR_CHANGE=re.compile(r'^%stoolchange'%COMMENT_PRE)
    COLOR_CHANGE_END=re.compile(r'^%sendchroma'%COMMENT_PRE)
    EXTRUDER_PATTERN=re.compile(r'^(G0?1\s+E%s)\s+F2400\s+'%FLOAT_PATTERN)
    EXTRUDER_REP='%s F200\r\n'

    def __init__(self,args):
        self.args=args
        self.func=self._scan
        self.lineNo=0
        
    def _scan(self,line):
        self.ofd.write(line)
        if self.COLOR_CHANGE.match(line):
            self.func=self._search

    def _search(self,line):
        m=self.EXTRUDER_PATTERN.match(line)
        if m:
            nline=self.EXTRUDER_REP%m.group(1)
            print 'line [%d] changing "%s" --> "%s"'%(self.lineNo,line.strip(),nline.strip())
            self.ofd.write(self.EXTRUDER_REP%m.group(1))
        else:
            self.ofd.write(line)
            if self.COLOR_CHANGE_END.match(line):
                self.func=self._scan

    def process(self):
        with open(args.output,'w') as self.ofd:
            with open(self.args.input,'r') as fd:
                for line in fd.readlines():
                    self.lineNo+=1
                    self.func(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='processing a palette gcode file')
    parser.add_argument('-i', '--input',help='input file ',required=True)
    parser.add_argument('-o', '--output',help='output file ',required=True)

    args = parser.parse_args()
    proc=Processor(args)
    proc.process()


