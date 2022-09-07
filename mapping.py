from utils import xprint
import valueType
import utils


class key_value:
    def __init__(self) -> None:
        self.identifier = None
        self.value_type = None
        self.plaintext_literal = None
        self.plaintext_identifier = None


class mapping:
    def __init__(self) -> None:
        self.identifier = None
        self.key = None
        self.value = None

    def read_key_value(self, component):
        component.identifier = utils.read_identifier(self)
        variant = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        component.bytecodes = self.bytecodes
        if variant == 0:
            component.value_type = valueType.valueType_name(1).name
        elif variant == 1:
            component.value_type = valueType.valueType_name(3)
        elif variant == 2:
            component.value_type = valueType.valueType_name(4)
        else:
            xprint("error")
        valueType.read_valueType_plaintext(component)
        self.bytecodes = component.bytecodes

    def disassemble_mapping(self, bytes):
        self.bytecodes = bytes
        self.identifier = utils.read_identifier(self)
        # Get key and value
        self.key = key_value()
        self.read_key_value(self.key)
        self.value = key_value()
        self.read_key_value(self.value)
        # xprint key and value
        xprint(
            f"key {self.key.identifier} as {self.key.plaintext_literal}.{self.key.value_type}"
        )
        xprint(
            f"value {self.value.identifier} as {self.value.plaintext_literal}.{self.value.value_type}"
        )
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
