from enum import Enum
from utils import xprint
import valueType
import utils


class entry:
    def __init__(self) -> None:
        self.bytecodes = None
        self.valueType = None
        self.identifier = None
        self.plaintext_literal = None
        self.plaintext_identifier = None


class record:
    def __init__(self) -> None:
        self.bytecodes = None
        self.entries = []
        self.identifier = None

    def set_record_gates_owner(self, identifier):
        new_entry = entry()
        new_entry.identifier = identifier
        value = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        new_entry.valueType = valueType.valueType_name((value == 1) + 1)
        new_entry.plaintext_literal = (
            valueType.LiteralType(12).name
            if (identifier == "gates")
            else valueType.LiteralType(0).name
        )
        return new_entry

    def read_record_num_entries(self):
        value = int.from_bytes(self.bytecodes[:2], "little")
        self.bytecodes = self.bytecodes[2:]
        return value

    def disassemble_record(self, bytes):
        self.bytecodes = bytes
        identifier = utils.read_identifier(self)
        owner = self.set_record_gates_owner("owner")
        gates = self.set_record_gates_owner("gates")
        self.entries.append(owner)
        self.entries.append(gates)
        xprint(f"record {identifier}")
        utils.tab += 1
        num_entries = self.read_record_num_entries()
        for _ in range(num_entries):
            new_entry = entry()
            new_entry.bytecodes = self.bytecodes
            new_entry.identifier = utils.read_identifier(new_entry)
            valueType.read_value_type(new_entry)
            self.entries.append(new_entry)
            # Set bytecodes used to the entry in the entry bytecodes
            rest_of_bytecodes = new_entry.bytecodes
            new_entry.bytecodes = self.bytecodes[
                : len(self.bytecodes) - len(rest_of_bytecodes)
            ]
            # remove used bytecodes for entry
            self.bytecodes = rest_of_bytecodes

        for new_entry in self.entries:
            xprint(
                f"{new_entry.identifier} as {new_entry.plaintext_literal}.{valueType.get_type(new_entry)} "
            )
        utils.tab -= 1
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
