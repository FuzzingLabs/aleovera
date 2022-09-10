from .utils import xadd
from . import valueType
from . import utils


class key_value:
    """
    Key_value class can contains the key or the value of the mapping.
    """

    def __init__(self, bytecodes) -> None:
        self.identifier = None
        self.attribute_type = None
        self.value = None
        self.read_key_value(bytecodes)

    def read_key_value(self, bytecodes):
        """Read the key or the value contents

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.identifier = utils.read_identifier(bytecodes)
        variant = bytecodes.read_u8()
        if variant == 0:
            self.attribute_type = valueType.attributeType(1).name
        elif variant == 1:
            self.attribute_type = valueType.attributeType(3).name
        elif variant == 2:
            self.attribute_type = valueType.attributeType(4).name
        else:
            print("error")
        self.value = valueType.read_plaintext(bytecodes)


class mapping:
    """
    The mapping class contains the key and the value mapped
    """

    def __init__(self, bytecodes) -> None:
        self.identifier = None
        self.key = None
        self.value = None
        self.disassemble_mapping(bytecodes)

    def pretty_print(self):
        """
        Pretty print all the content of the mapping
        """
        xadd(
            utils.color.CYAN + f"mapping {self.identifier}:" + utils.color.ENDC
        )
        utils.tab += 1
        xadd(
            utils.color.YELLOW
            + f"key {self.key.identifier}"
            + utils.color.ENDC
            + " as "
            + utils.color.GREEN
            + f"{self.key.value}.{self.key.attribute_type};"
            + utils.color.ENDC
        )
        xadd(
            utils.color.YELLOW
            + f"value {self.value.identifier}"
            + utils.color.ENDC
            + " as "
            + utils.color.GREEN
            + f"{self.value.value}.{self.value.attribute_type};"
            + utils.color.ENDC
        )
        utils.tab -= 1
        xadd()

    def disassemble_mapping(self, bytecodes):
        """Disassemble the mapping

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.identifier = utils.read_identifier(bytecodes)
        # Get key and value
        self.key = key_value(bytecodes)
        self.value = key_value(bytecodes)
        self.pretty_print()
