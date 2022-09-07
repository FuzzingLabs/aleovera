from IOregister import IOregister
from instruction import instruction
from utils import xprint
from finalize import finalize
import utils


class function:
    def __init__(self, type, bytecodes) -> None:
        # bytecodes contains the full bytecodes at the beginning, and is replaced by the bytecodes of the function only after the disassembly of this function
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
        return bytecodes.read_u16()

    def read_function_number_instructions(self, bytecodes):
        return bytecodes.read_u32()

    def read_IOregister(self, IO_type, bytecodes):
        new_register = IOregister(IO_type, bytecodes)
        self.registers.append(new_register)

    def read_instructions(self, bytecodes):
        new_instruction = instruction()
        new_instruction.disassemble_instructions(bytecodes)
        self.instructions.append(new_instruction)

    def read_finalize(self, bytecodes):
        new_finalize = finalize()
        #self.bytecodes = new_finalize.disassemble_finalize(self.bytecodes)
        new_finalize.disassemble_finalize(bytecodes)
        function_finalize = function(type="finalize")
        #self.bytecodes = function_finalize.disassemble_function(self.bytecodes)
        function_finalize.disassemble_function(bytecodes)
        self.finalizes.append(new_finalize)

    def pretty_print(self):
        xprint(f"{self.type} {self.identifier}")
        utils.tab += 1
        for i in range(self.number_inputs):
            self.registers[i].pretty_print()

        for instruction in self.instructions:
            xprint(instruction.disass)
        
        for i in range(self.number_outputs):
            self.registers[i + self.number_inputs].pretty_print()

        utils.tab -= 1


    def disassemble_function(self, bytecodes):
        self.identifier = utils.read_identifier(bytecodes)
        ###inputs
        self.number_inputs = self.read_function_number_IOregister(bytecodes)
        for _ in range(self.number_inputs):
            self.read_IOregister("input", bytecodes)
        ###instructions
        self.number_instructions = self.read_function_number_instructions(bytecodes)
        for _ in range(self.number_instructions):
            self.read_instructions(bytecodes)
        ###outputs
        self.number_outputs = self.read_function_number_IOregister(bytecodes)
        for _ in range(self.number_outputs):
            self.read_IOregister("output", bytecodes)
        ###finalize
        if self.type == "function" and len(bytecodes.bytecodes) > 0:
            is_finalize = bytecodes.read_u8()
            if is_finalize == 1:
                self.read_finalize(bytecodes)

        self.pretty_print()


