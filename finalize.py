from utils import xprint
from IOregister import IOregister
import valueType


class finalize:
    def __init__(self) -> None:
        self.bytecodes = None
        self.num_operands = None
        self.literal = None
        self.registers = []
        self.programID = None
        self.caller = None

    def read_IOregister(self, IO_type):
        new_input = IOregister(IO_type)
        self.bytecodes = new_input.disassemble_IOregister(self.bytecodes)
        self.registers.append(new_input)

    def read_operands(self):
        res = "finalize "
        for i in range(self.num_operands):
            variant = self.bytecodes[0]
            self.bytecodes = self.bytecodes[1:]
            if variant == 0:
                self.literal = valueType.read_plaintext_literal(self)
                xprint("todo1")
            elif variant == 1:
                self.read_IOregister("register")
                res += f"r{self.registers[-1].register_locator}"
                res += " "
            elif variant == 2:
                xprint("todo3")
            elif variant == 3:
                self.caller = "self.caller"
                res += self.caller
                res += " "
            else:
                xprint("error operand finalize")
        xprint(res)

    def disassemble_finalize(self, bytes):
        self.bytecodes = bytes
        self.num_operands = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        self.read_operands()
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
