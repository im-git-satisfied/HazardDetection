from Registers import Register
import re

class Instruction():
    def __init__(self, fields, instruction_str):
        self.operation = None
        self.target_reg = None
        self.arg_a = None
        self.arg_b = None
        self.ins_str = instruction_str
        self.fields = fields
        self.parse_fields()
        
        self.stall_str = "F-D-X-M-W"
        self.fw_str = "F-D-X-M-W"
        self.stalls = 0
        self.stalls_fw = 0
        

    def parse_fields(self):
        self.operation = self.fields[0] 
        self.target_reg = self.fields[1]
        self.arg_a = self.fields[2]
        
        if len(self.fields) == 4:
            self.arg_b = self.fields[3]
        else:
            self.ins_str = self.ins_str+"\t"
        
    def add_arg(self, arg):
        if arg.isdigit:
            return Register(value=arg)
        return Register(reg=arg)

    def stall(self, stalls):
        stall_char = "S-"
        stall_str = ""
        self.stalls = stalls
        if stalls > 0: 
            for stall in range(0, stalls):
                stall_str += stall_char
        
        self.stall_str = "F-{}D-X-M-W".format(stall_str)

    def stall_fw(self,stalls):
        stall_char = "S-"
        stall_str = ""
        self.stalls_fw = stalls
        if stalls > 0: 
            for stall in range(0, stalls):
                stall_str += stall_char

        self.fw_str = "F-{}D-X-M-W".format(stall_str)



    
