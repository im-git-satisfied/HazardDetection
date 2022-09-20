

class Register:
    def __init__(self):
        self.value = None
        self.needed = -1
        self.available = -1 
        self.avail_fw = -1
        self.ins_str = ""

    def set_ins_str(self, value):
        self.ins_str = value

    def set_needed(self,value):
        self.needed = value

    def set_available(self, value):
        self.available = value

    def set_avail_fw(self, value):
        self.avail_fw = value
    
    def set_value(self, value):
        self.available = value

    def print_register(self):
        print("value = ", self.value)
        print("needed: {} | available {}".format(self.needed, self.available))
