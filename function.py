from input import input
from instruction import instruction


class function:
    def __init__(self) -> None:
        # bytecodes contains the full bytecodes at the beginning, and is replaced by the bytecodes of the function only after the disassembly of this function
        self.bytecodes = None
        self.identifier = None
        self.number_inputs = None
        self.inputs = []
        self.number_instructions = None
        self.instructions = []

    def read_function_identifier(self):
        len_identifier = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        identifier = self.bytecodes[:len_identifier].decode("utf-8")
        self.bytecodes = self.bytecodes[len_identifier:]
        return identifier

    def read_function_number_inputs(self):
        number_inputs = int.from_bytes(self.bytecodes[:2], "little")
        self.bytecodes = self.bytecodes[2:]
        return number_inputs

    def read_function_number_instructions(self):
        res = int.from_bytes(self.bytecodes[:4], "little")
        self.bytecodes = self.bytecodes[4:]
        return res

    def read_inputs(self):
        new_input = input()
        self.bytecodes = new_input.disassemble_input(self.bytecodes)
        self.inputs.append(new_input)

    def read_instructions(self):
        new_instruction = instruction()
        self.bytecodes = new_instruction.disassemble_instruction(self.bytecodes)
        self.instructions.append(new_instruction)

    def disassemble_function(self, bytes):
        self.bytecodes = bytes
        self.identifier = self.read_function_identifier()
        print("func name : ", self.identifier)
        ###inputs
        self.number_inputs = self.read_function_number_inputs()
        print("number of inputs : ", self.number_inputs)
        print("---Inputs detected---")
        for i in range(self.number_inputs):
            self.read_inputs()
        ###instructions
        self.number_instructions = self.read_function_number_instructions()
        for i in range(self.number_instructions):
            self.read_instructions()
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
