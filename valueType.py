from enum import Enum, auto
import enum


class valueType_name(Enum):
    constant = 0
    public = auto()
    private = auto()
    record = auto()
    externalrecord = auto()


class valueType:
    def get_type(self, component):
        return valueType_name(component.valueType).name

    def read_plaintext_literal(self, component):
        res = component.bytecodes[:2]
        component.bytecodes = component.bytecodes[2:]
        return res

    def read_plaintext_identifier(self, component):
        res = component.bytecodes[0]
        component.bytecodes = component.bytecodes[1:]
        return res

    def read_valueType_plaintext(self, component):
        variant = component.bytecodes[0]
        component.bytecodes = component.bytecodes[1:]
        if variant == 0:
            component.valueType_literal = self.read_plaintext_literal(component)
        elif variant == 1:
            component.valueType_identifier = self.read_plaintext_identifier(
                component
            )

    def read_value_type(self, component):
        component.valueType = component.bytecodes[0]
        component.bytecodes = component.bytecodes[1:]
        if component.valueType == 0:
            self.read_valueType_plaintext(component)
        elif component.valueType == 1:
            self.read_valueType_plaintext(component)
        elif component.valueType == 2:
            self.read_valueType_plaintext(component)
        elif component.valueType == 3:
            print("record value type todo")
        elif component.valueType == 4:
            print("external record value type todo")
        else:
            print("fail ")
