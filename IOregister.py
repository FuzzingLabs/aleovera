from valueType import valueType


class IOregister:
    def __init__(self, IO_type) -> None:
        self.IO_type = IO_type
        self.bytecodes = None
        self.register_variant = None
        self.register_locator = None
        self.identifiers = []
        self.valueType = None
        self.valueType_literal = None
        self.valueType_identifier = None
        self.valueType_content = None

    def read_variable_length_integer(self):
        flag = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        if flag >= 0 and flag <= 252:
            return flag
        elif flag == 0xFD:
            self.bytecodes = self.bytecodes[2:]
            return 16
        elif flag == 0xFD:
            self.bytecodes = self.bytecodes[4:]
            return 32
        else:
            self.bytecodes = self.bytecodes[8:]
            return 64

    def disassemble_IOregister(self, bytes):
        self.bytecodes = bytes
        self.register_variant = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        self.register_locator = self.read_variable_length_integer()
        if self.register_variant == 1:
            num_identifiers = int.from_bytes(self.bytecodes[:2], "little")
            self.bytecodes = self.bytecodes[2:]
            for i in range(num_identifiers):
                self.identifiers.append(self.bytecodes[0])
                self.bytecodes = self.bytecodes[1:]
        elif self.register_variant != 0:
            print("error register_variant")
        ### get valueTYpe
        value_type = valueType()
        value_type.read_value_type(component=self)
        if self.valueType_literal != None:
            print(
                f"{self.IO_type} r{self.register_locator} as {self.valueType_literal}.{value_type.get_type(component=self)}"
            )
        elif self.valueType_identifier != None:
            print(
                f"{self.IO_type} r{self.register_locator} as {self.valueType_identifier}.{value_type.get_type(component=self)}"
            )
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
