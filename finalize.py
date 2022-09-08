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

    def disassemble_finalize(self, bytecodes):
        """Disassemble the finalize

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.num_operands = bytecodes.read_u8()
        self.operands = Operands(self.num_operands, bytecodes, False)
