from IOregister import IOregister
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
        self.number_outputs = None

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

    def disassemble_function(self, bytes):
        self.bytecodes = bytes
        self.identifier = self.read_function_identifier()
        print("func name : ", self.identifier)
        ###inputs
        self.number_inputs = self.read_function_number_IOregister()
        print("number of inputs : ", self.number_inputs)
        print("---Inputs detected---")
        for i in range(self.number_inputs):
            self.read_IOregister("input")
        ###instructions
        self.number_instructions = self.read_function_number_instructions()
        print("---Instructions detected---")
        for i in range(self.number_instructions):
            self.read_instructions()

        self.number_outputs = self.read_function_number_IOregister()
        print("number of outputs : ", self.number_outputs)
        print("---Outputs detected---")
        for i in range(self.number_outputs):
            self.read_IOregister("output")
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
