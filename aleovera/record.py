from .utils import xadd
from . import valueType
from . import utils
from .utils import xexit


class entry:
    """
    Element of a record
    """

    def __init__(self) -> None:
        self.identifier = None
        self.value = None
        self.attribute_type = None


class record:
    """
    Record class
    """

    def __init__(self, bytecodes) -> None:
        self.entries = []
        self.identifier = None
        self.disassemble_record(bytecodes)

    def pretty_print(self):
        """
        Pretty print all the content of the record
        """
        xadd(utils.color.CYAN + f"record {self.identifier}:" + utils.color.ENDC)
        utils.tab += 1
        for new_entry in self.entries:
            xadd(
                utils.color.YELLOW
                + f"{new_entry.identifier}"
                + utils.color.ENDC
                + " as "
                + utils.color.GREEN
                + f"{new_entry.value}.{new_entry.attribute_type.name};"
                + utils.color.ENDC
            )
        utils.tab -= 1
        xadd()

    def set_record_gates_owner(self, identifier, bytecodes):
        """Create the entry for the gates or the owner based on the identifier

        Args:
            identifier (String): Determines if it is an owner or a gates entry
            bytecodes (bytecodes): The bytecodes object

        Returns:
            entry: The new entry
        """
        new_entry = entry()
        new_entry.identifier = identifier
        value = bytecodes.read_u8()
        try:
            new_entry.attribute_type = valueType.attributeType((value == 1) + 1)
        except Exception as e:
            xexit()
        new_entry.value = (
            valueType.LiteralType(12).name
            if (identifier == "gates")
            else valueType.LiteralType(0).name
        )
        return new_entry

    def disassemble_record(self, bytecodes):
        """Disassemble the record

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.identifier = utils.read_identifier(bytecodes)
        owner = self.set_record_gates_owner("owner", bytecodes)
        gates = self.set_record_gates_owner("gates", bytecodes)
        self.entries.append(owner)
        self.entries.append(gates)
        num_entries = bytecodes.read_u16()
        for _ in range(num_entries):
            new_entry = entry()
            new_entry.identifier = utils.read_identifier(bytecodes)
            new_entry.attribute_type = valueType.read_value_type(bytecodes)
            new_entry.value = valueType.read_plaintext(bytecodes)
            self.entries.append(new_entry)
        self.pretty_print()
