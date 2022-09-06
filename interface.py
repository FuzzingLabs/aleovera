from enum import Enum
from valueType import valueType, valueType_name, LiteralType


class entry:
    def __init__(self) -> None:
        self.bytecodes = None
        self.valueType = None
        self.identifier = None
        self.valueType_literal = None
        self.valueType_identifier = None


class interface:
    def __init__(self) -> None:
        self.bytecodes = None
        self.entries = []
        self.identifier = None

    def read_identifier(self):
        len_identifier = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        identifier = self.bytecodes[:len_identifier].decode("utf-8")
        self.bytecodes = self.bytecodes[len_identifier:]
        return identifier

    def read_interface_num_entries(self):
        value = int.from_bytes(self.bytecodes[:2], "little")
        self.bytecodes = self.bytecodes[2:]
        return value

    def disassemble_interface(self, bytes):
        self.bytecodes = bytes
        identifier = self.read_identifier()
        print("interface name : ", identifier)
        num_entries = self.read_interface_num_entries()
        print("num of entries : ", num_entries)
        value_type = valueType()
        for i in range(num_entries):
            new_entry = entry()
            new_entry.identifier = self.read_identifier()
            new_entry.bytecodes = self.bytecodes
            value_type.read_valueType_plaintext(new_entry)
            self.entries.append(new_entry)
            # Set bytecodes used to the entry in the entry bytecodes
            rest_of_bytecodes = new_entry.bytecodes
            new_entry.bytecodes = self.bytecodes[
                : len(self.bytecodes) - len(rest_of_bytecodes)
            ]
            # remove used bytecodes for entry
            self.bytecodes = rest_of_bytecodes

        for new_entry in self.entries:
            print(f"{new_entry.identifier} as {new_entry.valueType_literal} ")

        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
