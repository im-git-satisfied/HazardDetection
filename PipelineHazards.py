#!/usr/bin/python3
from Program import Program
from Instruction import Instruction
import re
"""
Simple run file to open instructions.txt file and begin interpretation and writing to registers
"""


split_on = " |, "
remove   = "[\n\t]"
file = open('instructions.txt', 'r')
program = Program()

print(" #### Original Instructions ####\n") 

for line in file.readlines():

    if line:
        if line[0] != "#" and line != "\n":
            line = re.sub(remove, '', line.strip().upper())            
            print("\t" + line)
            fields = re.split(split_on, line)
            ins = Instruction(fields, line.strip("\n\t"))
            program.add_ins(ins)

program.run()
program.fw = True
program.registers = {}
program.run()



