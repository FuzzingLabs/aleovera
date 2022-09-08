from enum import Enum, auto
import utils


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


class attributeType(Enum):
    constant = 0
    public = auto()
    private = auto()
    record = auto()
    externalrecord = auto()


def read_plaintext_literal(bytecodes):
    """Get the literal type

    Args:
        bytecodes (bytecodes): The bytecodes object

    Returns:
        LiteralType: the LiteralType
    """
    res = bytecodes.read_u16()
    res = LiteralType(res).name
    return res


def read_plaintext(bytecodes):
    """Read an identifier or get the LiteralType based on the first byte

    Args:
        bytecodes (bytecodes): The bytecodes object

    Returns:
        LiteralType or String: The LiteralType or and identifier
    """
    variant = bytecodes.read_u8()
    if variant == 0:
        return read_plaintext_literal(bytecodes)
    elif variant == 1:
        return utils.read_identifier(bytecodes)


def read_value_type(bytecodes):
    """Get the attribyte type

    Args:
        bytecodes (bytecodes): The bytecodes object

    Returns:
        attributeType: the AttributeType
    """
    attribute_type = attributeType(bytecodes.read_u8())
    return attribute_type
