from enum import Enum
from utils import xprint
import valueType
import utils


class entry:
    def __init__(self) -> None:
        self.identifier = None
        self.value = None


class interface:
    def __init__(self, bytecodes) -> None:
        self.bytecodes = None
        self.entries = []
        self.identifier = None
        self.disassemble_interface(bytecodes)

    def read_interface_num_entries(self):
        value = self.bytecodes.read_u16()
        return value

    def pretty_print(self):
        xprint(f"identifier {self.identifier}")
        utils.tab += 1
        for new_entry in self.entries:
            xprint(f"{new_entry.identifier} as {new_entry.value}")
        utils.tab -= 1

    def disassemble_interface(self, bytecodes):
        self.bytecodes = bytecodes
        self.identifier = utils.read_identifier(bytecodes)
        num_entries = self.read_interface_num_entries()
        for _ in range(num_entries):
            new_entry = entry()
            new_entry.identifier = utils.read_identifier(self.bytecodes)
            new_entry.value = valueType.read_plaintext(self.bytecodes)
            self.entries.append(new_entry)
        self.pretty_print()
