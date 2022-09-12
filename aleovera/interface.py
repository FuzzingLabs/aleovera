from .utils import xadd
from . import valueType
from . import utils


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

    def fmt(self):
        """
        Pretty print all the content of the interface
        """
        xadd(
            utils.color.CYAN
            + f"interface {self.identifier}:"
            + utils.color.ENDC
        )
        utils.tab += 1
        for new_entry in self.entries:
            xadd(
                utils.color.YELLOW
                + f"{new_entry.identifier}"
                + utils.color.ENDC
                + " as "
                + utils.color.GREEN
                + f"{new_entry.value};"
                + utils.color.ENDC
            )
        utils.tab -= 1
        xadd()

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
        self.fmt()
