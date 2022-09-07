from valueType import valueType_name, valueType


class key:
    def __init__(self) -> None:
        self.bytecodes = None
        self.identifier = None
        self.value_type = None
        self.valueType_literal = None
        self.valueType_identifier = None


class value:
    def __init__(self) -> None:
        self.bytecodes = None
        self.identifier = None
        self.value_type = None
        self.valueType_literal = None
        self.valueType_identifier = None


class mapping:
    def __init__(self) -> None:
        self.bytecodes = None
        self.identifier = None
        self.key = None
        self.value = None

    def read_identifier(self):
        len_identifier = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        identifier = self.bytecodes[:len_identifier].decode("utf-8")
        self.bytecodes = self.bytecodes[len_identifier:]
        return identifier

    def read_key_value(self, component):
        component.identifier = self.read_identifier()
        variant = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        value_type = valueType()
        component.bytecodes = self.bytecodes
        value_type = valueType()
        if variant == 0:
            component.value_type = valueType_name(1).name
        elif variant == 1:
            component.value_type = valueType_name(3)
        elif variant == 2:
            component.value_type = valueType_name(4)
        else:
            print("error")
        value_type.read_valueType_plaintext(component)
        self.bytecodes = component.bytecodes

    def disassemble_mapping(self, bytes):
        self.bytecodes = bytes
        self.identifier = self.read_identifier()
        new_key = key()
        self.read_key_value(new_key)
        self.key = new_key
        new_value = value()
        self.read_key_value(new_value)
        self.value = new_value
        print(
            f"key {new_key.identifier} as {new_key.valueType_literal}.{new_key.value_type}"
        )
        print(
            f"value {new_value.identifier} as {new_value.valueType_literal}.{new_value.value_type}"
        )
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
