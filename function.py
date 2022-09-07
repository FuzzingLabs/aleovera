from IOregister import IOregister
from instruction import instruction
from utils import xprint
from finalize import finalize
import utils


class function:
    def __init__(self, type, bytecodes) -> None:
        # bytecodes contains the full bytecodes at the beginning, and is replaced by the bytecodes of the function only after the disassembly of this function
        self.type = type
        self.bytecodes = None
        self.identifier = None
        self.number_inputs = None
        self.registers = []
        self.number_instructions = None
        self.instructions = []
        self.number_outputs = None
        self.finalizes = []
        self.disassemble_function(bytecodes)

    def read_function_number_IOregister(self):
        return self.bytecodes.read_u16()

    def read_function_number_instructions(self):
        return self.bytecodes.read_u32()

    def read_IOregister(self, IO_type):
        new_register = IOregister(IO_type, self.bytecodes)
        self.registers.append(new_register)

    def read_instructions(self):
        new_instruction = instruction()
        self.bytecodes = new_instruction.disassemble_instruction(self.bytecodes)
        self.instructions.append(new_instruction)

    def read_finalize(self):
        new_finalize = finalize()
        self.bytecodes = new_finalize.disassemble_finalize(self.bytecodes)
        function_finalize = function(type="finalize")
        self.bytecodes = function_finalize.disassemble_function(self.bytecodes)
        self.finalizes.append(new_finalize)

    def pretty_print(self):
        xprint(f"{self.type} {self.identifier}")
        utils.tab += 1
        for new_input in self.registers:
            new_input.pretty_print()
        print("MAXIME DON'T FORGET TO MOVE IT AT THE END OF THE FUNCTION")

    def disassemble_function(self, bytecodes):
        self.bytecodes = bytecodes
        self.identifier = utils.read_identifier(self.bytecodes)
        ###inputs
        self.number_inputs = self.read_function_number_IOregister()
        for _ in range(self.number_inputs):
            self.read_IOregister("input")
        ###instructions
        self.pretty_print()  #### MAXIME DON'T FORGET TO MOVE IT AT THE END OF THE FUNCTION
        self.number_instructions = self.read_function_number_instructions()
        for _ in range(self.number_instructions):
            self.read_instructions()
        ###outputs
        self.number_outputs = self.read_function_number_IOregister()
        for _ in range(self.number_outputs):
            self.read_IOregister("output")
        ###finalize
        if self.type == "function" and len(self.bytecodes) > 0:
            is_finalize = self.bytecodes.read_u8()
            if is_finalize == 1:
                self.read_finalize()
