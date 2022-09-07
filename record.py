from enum import Enum
from utils import xprint
import bytecodes
import valueType
import utils


class entry:
    def __init__(self) -> None:
        self.identifier = None
        self.value = None
        self.attribute_type = None


class record:
    def __init__(self, bytecodes) -> None:
        self.entries = []
        self.identifier = None
        self.disassemble_record(bytecodes)

    def pretty_print(self):
        xprint(f"record {self.identifier}")
        utils.tab += 1
        for new_entry in self.entries:
            xprint(
                f"{new_entry.identifier} as {new_entry.value}.{new_entry.attribute_type.name} "
            )
        utils.tab -= 1

    def set_record_gates_owner(self, identifier, bytecodes):
        new_entry = entry()
        new_entry.identifier = identifier
        value = bytecodes.read_u8()
        new_entry.attribute_type = valueType.attributeType((value == 1) + 1)
        new_entry.value = (
            valueType.LiteralType(12).name
            if (identifier == "gates")
            else valueType.LiteralType(0).name
        )
        return new_entry

    def disassemble_record(self, bytecodes):
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
