from utils import xprint
from register import register
import utils
import valueType


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
        if self.attribute_type != valueType.attributeType.record:
            res += f"{self.value}.{valueType.attributeType(self.attribute_type).name}"
        else:
            res += f"{self.value}"
        res += ";"
        xprint(res)

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
            print(
                "external record value type todo : /home/nabih/snarkVM-fuzzinglabs/console/program/src/data_types/value_type/bytes.rs"
            )
        else:
            print("fail")
