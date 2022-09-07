from utils import xprint
import valueType
import utils


class key_value:
    def __init__(self, bytecodes) -> None:
        self.identifier = None
        self.attribute_type = None
        self.value = None
        self.read_key_value(bytecodes)

    def read_key_value(self, bytecodes):
        self.identifier = utils.read_identifier(bytecodes)
        variant = bytecodes.read_u8()
        if variant == 0:
            self.attribute_type = valueType.attributeType(1).name
        elif variant == 1:
            self.attribute_type = valueType.attributeType(3).name
        elif variant == 2:
            self.attribute_type = valueType.attributeType(4).name
        else:
            xprint("error")
        self.value = valueType.read_plaintext(bytecodes)


class mapping:
    def __init__(self, bytecodes) -> None:
        self.identifier = None
        self.key = None
        self.value = None
        self.disassemble_mapping(bytecodes)

    def pretty_print(self):
        xprint(f"mapping {self.identifier}:")
        utils.tab += 1
        xprint(
            f"key {self.key.identifier} as {self.key.value}.{self.key.attribute_type}"
        )
        xprint(
            f"value {self.value.identifier} as {self.value.value}.{self.value.attribute_type}"
        )
        utils.tab -= 1

    def disassemble_mapping(self, bytecodes):
        self.identifier = utils.read_identifier(bytecodes)
        # Get key and value
        self.key = key_value(bytecodes)
        self.value = key_value(bytecodes)
        self.pretty_print()
