from enum import Enum, auto
from . import utils
from .operand import Operands


class Opcode(Enum):
    decrement = 0
    not_implemented = auto()
    increment = auto()


class finalize_instruction:
    """
    The instruction class
    """

    def __init__(self, opcode) -> None:
        self.opcode = opcode
        self.mapping = None
        self.first = None
        self.second = None

    def fmt(self):
        """Get the disassembly of the instruction

        Returns:
            String: The disassembly of the instruction
        """
        return (
            utils.color.RED
            + f"{Opcode(self.opcode).name}"
            + utils.color.ENDC
            + f" {self.mapping}[{self.first.fmt()}] by {self.second.fmt()};"
        )

    def disassemble_finalize_instruction(self, bytecodes):
        """Disassemble the instruction

        Args:
            bytecodes (bytecodes): The bytecodes object
        """

        self.mapping = utils.read_identifier(bytecodes)
        operands_list = Operands(2, bytecodes)
        self.first = operands_list.operands[0]
        self.second = operands_list.operands[1]
