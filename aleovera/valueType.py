from enum import Enum, auto
from types import DynamicClassAttribute
from .utils import xexit
from . import utils


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

    @DynamicClassAttribute
    def name(self):
        """The name of the Enum member."""
        return self._name_.lower()


class attributeType(Enum):
    constant = 0
    public = auto()
    private = auto()
    record = auto()
    externalrecord = auto()


class attributeType_finalize(Enum):
    public = 0
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
    try:
        res = LiteralType(res).name
        return res
    except Exception as e:
        xexit()


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


def read_finalize_value_type(bytecodes):
    """Get the attribyte type of a finalize IOregister

    Args:
        bytecodes (bytecodes): The bytecodes object

    Returns:
        attributeType: the AttributeType
    """
    try:
        attribute_type = attributeType_finalize(bytecodes.read_u8())
    except Exception:
        xexit()

    if attribute_type == attributeType_finalize.public:
        value = read_plaintext(bytecodes)
    if attribute_type == attributeType_finalize.record:
        value = utils.read_identifier(bytecodes)
    if attribute_type == attributeType_finalize.externalrecord:
        value = utils.read_locator(bytecodes)
    return (attribute_type, value)


def read_function_value_type(bytecodes):
    attribute_type = read_value_type(bytecodes)
    try:
        attributeType(attribute_type)
    except Exception:
        xexit()
    if (
        attribute_type == attributeType.constant
        or attribute_type == attributeType.public
        or attribute_type == attributeType.private
    ):
        value = read_plaintext(bytecodes)
    elif attribute_type == attributeType.record:
        value = utils.read_identifier(bytecodes)
    elif attribute_type == attributeType.externalrecord:
        read_external = utils.read_external(bytecodes)
        value = read_external[0].fmt() + "/" + read_external[1]
    return (attribute_type, value)


def read_closure_register_type(bytecodes):
    variant = bytecodes.read_u8()
    type = [0, 1, 2]
    #### Check if variant is a plaintext,identifier or locator, if it's not, call xexit
    try:
        type[variant]
    except Exception:
        xexit()
    if variant == 0:
        return read_plaintext(bytecodes)
    elif variant == 1:
        return utils.read_identifier(bytecodes)
    elif variant == 2:
        return utils.read_locator(bytecodes)


def read_value_type(bytecodes):
    """Get the attribyte type

    Args:
        bytecodes (bytecodes): The bytecodes object

    Returns:
        attributeType: the AttributeType
    """
    try:
        return attributeType(bytecodes.read_u8())
    except Exception as e:
        xexit()
