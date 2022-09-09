from .utils import xadd
from .register import register
from . import utils
from . import valueType


class IOregister:
    """
    The IOregister class. Can be an input or an output.
    """

    def __init__(self, IO_type, bytecodes, finalize=False) -> None:
        self.IO_type = IO_type
        self.finalize = finalize
        self.value = None
        self.attribute_type = None
        self.register = None
        self.disassemble_IOregister(bytecodes)

    def pretty_print(self):
        """
        Pretty print all the content of the IOregister
        """
        res = f"{self.IO_type} r{self.register.locator} as "
        if (
            self.attribute_type != valueType.attributeType.record
            and self.attribute_type != valueType.attributeType.externalrecord
        ):
            if (
                self.value == "Field"
                and self.attribute_type == valueType.attributeType.constant
            ):
                res += f"{self.value}"
            else:
                res += f"{self.value}.{valueType.attributeType(self.attribute_type).name}"
        else:
            res += f"{self.value}.record"
        res += ";"
        xadd(res)

    def disassemble_IOregister(self, bytecodes):
        """Disassemble the IOregister

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.register = register(bytecodes)
        ### get valueType
        if self.finalize:
            self.attribute_type = valueType.read_finalize_value_type(bytecodes)
        else:
            self.attribute_type = valueType.read_value_type(bytecodes)
        if (
            self.attribute_type == valueType.attributeType.constant
            or self.attribute_type == valueType.attributeType.public
            or self.attribute_type == valueType.attributeType.private
        ):
            self.value = valueType.read_plaintext(bytecodes)
        elif self.attribute_type == valueType.attributeType.record:
            self.value = utils.read_identifier(bytecodes)
        elif self.attribute_type == valueType.attributeType.externalrecord:
            read_external = utils.read_external(bytecodes)
            self.value = read_external[0].fmt() + "/" + read_external[1]
        else:
            print("fail")
