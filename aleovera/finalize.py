from .utils import xadd
from .IOregister import IOregister
from .instruction import instruction
from .finalize_instruction import finalize_instruction
from .operand import Operands
from . import utils
import sys


class finalize_function:
    def __init__(self, bytecodes) -> None:
        self.identifier = None
        self.number_inputs = None
        self.registers = []
        self.number_commands = None
        self.instructions = []
        self.number_outputs = None
        self.finalizes = []
        self.disassemble_finalize_function(bytecodes)

    def read_finalize_function_number_IOregister(self, bytecodes):
        """Read the number of IOregister (inputs or outputs)

        Args:
            bytecodes (bytecodes): The bytecodes object

        Returns:
            Int: The number of IOregister
        """
        return bytecodes.read_u16()

    def read_finalize_function_number_commands(self, bytecodes):
        return bytecodes.read_u16()

    def read_finalize_function_number_instructions(self, bytecodes):
        """Read the number of instructions

        Args:
            bytecodes (bytecodes): The bytecodes object

        Returns:
            Int: The number of instruction
        """
        return bytecodes.read_u32()

    def read_IOregister(self, IO_type, bytecodes):
        """Read the IOregister (inputs or outputs)

        Args:
            IO_type (String): the IO_type (input/output)
            bytecodes (bytecodes): The bytecodes object
        """
        new_register = IOregister(IO_type, bytecodes, finalize=True)
        self.registers.append(new_register)

    def read_commands(self, bytecodes):
        variant = bytecodes.read_u8()
        if variant == 1:
            self.read_instruction(bytecodes)
        elif variant == 0 or variant == 2:
            self.read_finalize_instruction(bytecodes, variant)
        else:
            sys.exit("Error command does not exist")

    def read_finalize_instruction(self, bytecodes, opcode):
        new_finalize_instruction = finalize_instruction(opcode)
        new_finalize_instruction.disassemble_finalize_instruction(bytecodes)
        self.instructions.append(new_finalize_instruction)

    def read_instruction(self, bytecodes):
        """Read the instruction

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        new_instruction = instruction()
        new_instruction.disassemble_instruction(bytecodes)
        self.instructions.append(new_instruction)

    def pretty_print(self):
        """
        Pretty print all the content of the function
        """
        xadd(
            utils.color.BLUE + f"finalize {self.identifier}:" + utils.color.ENDC
        )
        utils.tab += 1
        for i in range(self.number_inputs):
            self.registers[i].pretty_print()

        for instruction in self.instructions:
            xadd(instruction.fmt())

        for i in range(self.number_outputs):
            self.registers[i + self.number_inputs].pretty_print()

        utils.tab -= 1

    def disassemble_finalize_function(self, bytecodes):
        """Disassemble the function

        Args:
            bytecodes (_type_): _description_
        """
        self.identifier = utils.read_identifier(bytecodes)
        ###inputs
        self.number_inputs = self.read_finalize_function_number_IOregister(
            bytecodes
        )
        for _ in range(self.number_inputs):
            self.read_IOregister("input", bytecodes)
        ###commands
        self.number_commands = self.read_finalize_function_number_commands(
            bytecodes
        )
        for _ in range(self.number_commands):
            self.read_commands(bytecodes)
        ###outputs
        self.number_outputs = self.read_finalize_function_number_IOregister(
            bytecodes
        )
        for _ in range(self.number_outputs):
            self.read_IOregister("output", bytecodes)


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
        self.function = None

    def disassemble_finalize(self, bytecodes):
        """Disassemble the finalize

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.num_operands = bytecodes.read_u8()
        self.operands = Operands(self.num_operands, bytecodes, False)
        self.function = finalize_function(bytecodes)
