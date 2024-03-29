from .IOregister import IOregister
from .instruction import instruction
from .finalize import finalize
from .utils import xadd
from . import utils


class function:
    def __init__(self, type, bytecodes) -> None:
        self.type = type
        self.identifier = None
        self.number_inputs = None
        self.registers = []
        self.number_instructions = None
        self.instructions = []
        self.number_outputs = None
        self.finalizes = []
        self.disassemble_function(bytecodes)

    def read_function_number_IOregister(self, bytecodes):
        """Read the number of IOregister (inputs or outputs)

        Args:
            bytecodes (bytecodes): The bytecodes object

        Returns:
            Int: The number of IOregister
        """
        return bytecodes.read_u16()

    def read_function_number_instructions(self, bytecodes):
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
        new_register = IOregister(
            IO_type,
            bytecodes,
            closure=self.type == "closure",
            function=self.type == "function",
        )
        self.registers.append(new_register)

    def read_instruction(self, bytecodes):
        """Read the instruction

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        new_instruction = instruction()
        new_instruction.disassemble_instruction(bytecodes)
        self.instructions.append(new_instruction)

    def read_finalize(self, bytecodes):
        """Read the finalize

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        new_finalize = finalize()
        new_finalize.disassemble_finalize(bytecodes)
        #        function_finalize = function(type="finalize")
        #        function_finalize.disassemble_function(bytecodes)
        self.finalizes.append(new_finalize)

    def fmt(self):
        """
        Pretty print all the content of the function
        """
        xadd(
            utils.color.HEADER
            + f"{self.type} {self.identifier}:"
            + utils.color.ENDC
        )
        utils.tab += 1
        for i in range(self.number_inputs):
            self.registers[i].fmt()

        for instruction in self.instructions:
            xadd(instruction.fmt())

        for i in range(self.number_outputs):
            self.registers[i + self.number_inputs].fmt()

        if self.finalizes:
            xadd(f"finalize {self.finalizes[0].operands.fmt()};")
            utils.tab -= 1
            if (utils.tab < 0):
                utils.tab = 0
            xadd("")
        if len(self.finalizes) != 0:
            for finalize in self.finalizes:
                finalize.function.fmt()
        else:
            utils.tab -= 1
        xadd("")

    def disassemble_function(self, bytecodes):
        """Disassemble the function

        Args:
            bytecodes (_type_): _description_
        """
        self.identifier = utils.read_identifier(bytecodes)
        ###inputs
        self.number_inputs = self.read_function_number_IOregister(bytecodes)
        for _ in range(self.number_inputs):
            self.read_IOregister("input", bytecodes)
        ###instructions
        self.number_instructions = self.read_function_number_instructions(
            bytecodes
        )
        for _ in range(self.number_instructions):
            self.read_instruction(bytecodes)
        ###outputs
        self.number_outputs = self.read_function_number_IOregister(bytecodes)
        for _ in range(self.number_outputs):
            self.read_IOregister("output", bytecodes)
        ###finalize
        if self.type == "function" and len(bytecodes.bytecodes) > 0:
            is_finalize = bytecodes.read_u8()
            if is_finalize == 1:
                self.read_finalize(bytecodes)
        self.fmt()
