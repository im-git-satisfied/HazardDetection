from Registers import Register
from Instruction import Instruction
import re

class Program:
    def __init__(self):
        self.registers = {}
        self.counter = 0
        self.cycle = 0
        self.instructions = []
        self.instruction_counter = 0
        self.curr_ins = None
        self.fw = False

    # Register / Instruction Functions 
    
    # program functions 
    def run(self):
        if self.fw:
            print("\n ####          Forwarding Unit Hazard Identification       ####\n")
        else:
            print("\n ####       No Forwarding Unit Hazard Identification       ####\n")
        for item in self.instructions:
            
            self.curr_ins = item
            self.fetch_ins()
            self.counter += 1
            self.cycle += 1
        
        if self.fw:
            self.run_with_fw()
        else:
            self.run_with_stalls()
        self.counter = 0
        self.cycle = 0

    def fetch_ins(self):

        self.print_ins()
        
        self.decode_reg(self.curr_ins.arg_a)
        self.decode_reg(self.curr_ins.arg_b)
        if self.curr_ins.operation in ["LD", "LW", "SD", "SW"]:
            self.decode_reg(self.curr_ins.target_reg)
        #self.decode_reg(self.curr_ins.target_reg)
        self.execute_ins()
        

    def decode_reg(self, register):
        # do I have a nonetype?
        add = True

        if register:
            if "(" in register:
                add = False
                register = re.sub("^\d\(", "", register).strip("\)")
            if not register.isdigit():

                reg_obj = self.registers.get(register)

                if reg_obj:
                    self.hazard_check(register, reg_obj)
                else:
                    self.add_register(register)
        return 


    def execute_ins(self):
        tar_reg = self.registers.get(self.curr_ins.target_reg)

        if not tar_reg:
            self.add_register(self.curr_ins.target_reg)
        self.set_availability()
        self.memory_ins()

    def memory_ins(self):
        #print("writing to memory")
        self.write_ins()

    def write_ins(self):
        # print("writing to register")
        self.instructions[self.counter] = self.curr_ins

    def run_with_stalls(self):
        print("\n ####       Stalls Without Forwarding Unit         #####\n")
        self.cycles = 0
        self.counter = 0
        for item in self.instructions:
            self.curr_ins = item
            self.print_ins()
            self.counter += 1
            if self.curr_ins.stalls > 0:
                self.counter += (self.curr_ins.stalls)

    def run_with_fw(self):
        print("\n ####       With Forwarding Unit       #####\n")
        self.cycles = 0
        self.counter = 0
        for item in self.instructions:
            self.curr_ins = item
            self.print_ins()
            self.counter += 1
            if self.curr_ins.stalls_fw > 0:
                self.counter += (self.curr_ins.stalls_fw)
         
    def hazard_check(self, reg, reg_obj):
        fw_str = "\t\tFW Data Hazard for {} from {}"
        no_fw_str = "\t\tData Hazard for {} from {}"
        hazard_str = None
        curr_stalls = 0
        stall_func = None

        if self.fw:
            stalls = reg_obj.avail_fw - (self.cycle+3)
            hazard_str = fw_str
            curr_stalls = self.curr_ins.stalls_fw
            stall_func = self.curr_ins.stall_fw
        else:
            stalls = reg_obj.available - (self.cycle + 2)
            hazard_str = no_fw_str
            curr_stalls = self.curr_ins.stalls
            stall_func = self.curr_ins.stall

        if stalls > 0:
            print(hazard_str.format(reg, reg_obj.ins_str))
            self.cycle += stalls
            # a single register stall should resolve both
            if curr_stalls == 0:
                stall_func(stalls)

        return 

    def fw_hazard_check(self,arg,reg):
        if stalls > 0:
            print("\tFW Data Hazard Detected", reg)
            self.cycle += stalls
            if self.curr_ins.stalls_fw == 0:
                self.curr_ins.stall_fw(stalls)
        return

    # utility functions 
    def print_ins(self):
        cycle_str="  "
        ins_str = ""
        for x in range(0,self.counter):
            ins_str += cycle_str

        if self.fw:
            print("\t{}\t|{}{}".format(self.curr_ins.ins_str, ins_str, self.curr_ins.fw_str))
        else:
            print("\t{}\t|{}{}".format(self.curr_ins.ins_str, ins_str, self.curr_ins.stall_str))

    def add_ins(self, instruction):
        self.instructions.append(instruction)
 
    def add_register(self, reg):
        self.registers[reg] = Register()

    def set_availability(self):

        if self.fw:
            if self.curr_ins.operation in ["ADD", "SUB", "MUL", "DIV", "ADDI", "DIVI", "MULI", "SUBI"]:
                self.registers[self.curr_ins.target_reg].set_avail_fw(self.cycle+4)

            if self.curr_ins.operation in ["LD", "SW", "LW", "SD"]:
                self.registers[self.curr_ins.target_reg].set_avail_fw(self.cycle+5)

        else:        
            if self.curr_ins.operation in ["SW", "SD"]:
                self.registers[self.curr_ins.target_reg].set_available(self.cycle)
            else:
                self.registers[self.curr_ins.target_reg].set_available(self.cycle + 5)

        self.registers[self.curr_ins.target_reg].ins_str = self.curr_ins.ins_str

