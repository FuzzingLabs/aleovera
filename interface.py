from enum import Enum
from utils import xprint
import valueType
import utils


class entry:
    """
    Element of an interface
    """

    def __init__(self) -> None:
        self.identifier = None
        self.value = None


class interface:
    """
    Interface class
    """

    def __init__(self, bytecodes) -> None:
        self.bytecodes = None
        self.entries = []
        self.identifier = None
        self.disassemble_interface(bytecodes)

    def read_interface_num_entries(self):
        """Read the number of entries in the interface

        Returns:
            Int: The number of entries in the interface
        """
        value = self.bytecodes.read_u16()
        return value

    def pretty_print(self):
        """
        Pretty print all the content of the interface
        """
        xprint(f"identifier {self.identifier}")
        utils.tab += 1
        for new_entry in self.entries:
            xprint(f"{new_entry.identifier} as {new_entry.value}")
        utils.tab -= 1

    def disassemble_interface(self, bytecodes):
        """Disassemble the interface

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.bytecodes = bytecodes
        self.identifier = utils.read_identifier(bytecodes)
        num_entries = self.read_interface_num_entries()
        for _ in range(num_entries):
            new_entry = entry()
            new_entry.identifier = utils.read_identifier(self.bytecodes)
            new_entry.value = valueType.read_plaintext(self.bytecodes)
            self.entries.append(new_entry)
        self.pretty_print()
