from IOregister import IOregister
from instruction import instruction
from utils import xprint
from finalize import finalize
import utils


class function:
    def __init__(self, type) -> None:
        # bytecodes contains the full bytecodes at the beginning, and is replaced by the bytecodes of the function only after the disassembly of this function
        self.type = type
        self.bytecodes = None
        self.identifier = None
        self.number_inputs = None
        self.inputs = []
        self.number_instructions = None
        self.instructions = []
        self.number_outputs = None
        self.finalizes = []

    def read_function_identifier(self):
        len_identifier = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        identifier = self.bytecodes[:len_identifier].decode("utf-8")
        self.bytecodes = self.bytecodes[len_identifier:]
        return identifier

    def read_function_number_IOregister(self):
        number_inputs = int.from_bytes(self.bytecodes[:2], "little")
        self.bytecodes = self.bytecodes[2:]
        return number_inputs

    def read_function_number_instructions(self):
        res = int.from_bytes(self.bytecodes[:4], "little")
        self.bytecodes = self.bytecodes[4:]
        return res

    def read_IOregister(self, IO_type):
        new_input = IOregister(IO_type)
        self.bytecodes = new_input.disassemble_IOregister(self.bytecodes)
        self.inputs.append(new_input)

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

    def disassemble_function(self, bytes):
        self.bytecodes = bytes
        self.identifier = self.read_function_identifier()
        xprint(f"{self.type} {self.identifier} : ")
        utils.tab += 1
        ###inputs
        self.number_inputs = self.read_function_number_IOregister()
        for i in range(self.number_inputs):
            self.read_IOregister("input")
        ###instructions
        self.number_instructions = self.read_function_number_instructions()
        for i in range(self.number_instructions):
            self.read_instructions()
        ###outputs
        self.number_outputs = self.read_function_number_IOregister()
        for i in range(self.number_outputs):
            self.read_IOregister("output")
        ###finalize
        if self.type == "function" and len(self.bytecodes) > 0:
            is_finalize = self.bytecodes[0]
            self.bytecodes = self.bytecodes[1:]
            if is_finalize == 1:
                self.read_finalize()
        utils.tab -= 1
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
