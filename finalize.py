from utils import xprint
from register import register
from operand import Operand, Operands, OperandType
import valueType


class finalize:
    """
    The finalize class
    """

    def __init__(self) -> None:
        self.num_operands = None
        self.literal = None
        self.registers = []
        self.programID = None
        self.caller = None
        self.operands = []

    # def read_register(self):
    #     new_input = register()
    #     self.bytecodes = new_input.disassemble_register(self.bytecodes)
    #     self.registers.append(new_input)

    # def read_operands(self):
    #     res = "finalize "
    #     for i in range(self.num_operands):
    #         variant = self.bytecodes[0]
    #         self.bytecodes = self.bytecodes[1:]
    #         if variant == 0:
    #             self.literal = valueType.read_plaintext_literal(self)
    #             xprint("todo1")
    #         elif variant == 1:
    #             self.read_IOregister("register")
    #             res += f"r{self.registers[-1].register_locator}"
    #             res += " "
    #         elif variant == 2:
    #             xprint("todo3")
    #         elif variant == 3:
    #             self.caller = "self.caller"
    #             res += self.caller
    #             res += " "
    #         else:
    #             xprint("error operand finalize")
    #     xprint(res)

    def disassemble_finalize(self, bytecodes):
        """Disassemble the finalize

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.num_operands = bytecodes.read_u8()
        self.operands = Operands(self.num_operands, bytecodes, False)
