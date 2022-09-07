from utils import xprint
import valueType


class IOregister:
    def __init__(self, IO_type) -> None:
        self.IO_type = IO_type
        self.bytecodes = None
        self.register_locator = None
        self.identifiers = []
        self.plaintext_literal = None
        self.plaintext_identifier = None
        self.record_identifier = None

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
        variant = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        self.register_locator = self.read_variable_length_integer()
        if variant == 1:
            num_identifiers = int.from_bytes(self.bytecodes[:2], "little")
            self.bytecodes = self.bytecodes[2:]
            for _ in range(num_identifiers):
                self.identifiers.append(self.bytecodes[0])
                self.bytecodes = self.bytecodes[1:]
        elif variant != 0:
            xprint("error register_variant")
        ### get valueType
        if self.IO_type != "register":
            valueType.read_value_type(component=self)
            res = f"{self.IO_type} r{self.register_locator} as "
            if self.plaintext_literal != None:
                res += f"{self.plaintext_literal}.{valueType.get_type(component=self)}"
            elif self.plaintext_identifier != None:
                res += f"{self.plaintext_identifier}.{valueType.get_type(component=self)}"
            elif self.record_identifier != None:
                res += f"{self.record_identifier}"
        xprint(res)
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
