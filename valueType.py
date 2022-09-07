from utils import xprint
from enum import Enum, auto


class LiteralType(Enum):
    # The Aleo address type.
    Address = 0
    # The boolean type.
    Boolean = auto()
    # The field type (base field).
    Field = auto()
    # The group type (affine).
    Group = auto()
    # The 8-bit signed integer type.
    I8 = auto()
    # The 16-bit signed integer type.
    I16 = auto()
    # The 32-bit signed integer type.
    I32 = auto()
    # The 64-bit signed integer type.
    I64 = auto()
    # The 128-bit signed integer type.
    I128 = auto()
    # The 8-bit unsigned integer type.
    U8 = auto()
    # The 16-bit unsigned integer type.
    U16 = auto()
    # The 32-bit unsigned integer type.
    U32 = auto()
    # The 64-bit unsigned integer type.
    U64 = auto()
    # The 128-bit unsigned integer type.
    U128 = auto()
    # The scalar type (scalar field).
    Scalar = auto()
    # The string type.
    String = auto()


class valueType_name(Enum):
    constant = 0
    public = auto()
    private = auto()
    record = auto()
    externalrecord = auto()


def get_type(component):
    return valueType_name(component.valueType).name


def read_plaintext_literal(component):
    res = component.bytecodes[:2]
    component.bytecodes = component.bytecodes[2:]
    res = LiteralType(int.from_bytes(res, "little")).name
    return res


def read_plaintext_identifier(component):
    length = component.bytecodes[0]
    component.bytecodes = component.bytecodes[1:]
    res = component.bytecodes[:length]
    component.bytecodes = component.bytecodes[length:]
    return res.decode("utf-8")


def read_valueType_plaintext(component):
    variant = component.bytecodes[0]
    component.bytecodes = component.bytecodes[1:]
    if variant == 0:
        component.plaintext_literal = read_plaintext_literal(component)
    elif variant == 1:
        component.plaintext_identifier = read_plaintext_identifier(component)


def read_record_identifier(component):
    length = component.bytecodes[0]
    component.bytecodes = component.bytecodes[1:]
    res = component.bytecodes[:length]
    component.bytecodes = component.bytecodes[length:]
    component.record_identifier = res.decode("utf-8")


def read_value_type(component):
    component.valueType = component.bytecodes[0]
    component.bytecodes = component.bytecodes[1:]
    if component.valueType == 0:
        read_valueType_plaintext(component)
    elif component.valueType == 1:
        read_valueType_plaintext(component)
    elif component.valueType == 2:
        read_valueType_plaintext(component)
    elif component.valueType == 3:
        read_record_identifier(component)
    elif component.valueType == 4:
        xprint("external record value type todo")
    else:
        xprint("fail ")
