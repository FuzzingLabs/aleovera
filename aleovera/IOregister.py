from .utils import xadd, xexit
from .register import register
from . import utils
from . import valueType


class IOregister:
    """
    The IOregister class. Can be an input or an output.
    """

    def __init__(
        self, IO_type, bytecodes, closure=False, finalize=False, function=False
    ) -> None:
        self.IO_type = IO_type
        self.finalize = finalize
        self.function = function
        self.closure = closure
        self.value = None
        self.attribute_type = None
        self.register = None
        self.disassemble_IOregister(bytecodes)

    def fmt(self):
        """
        Pretty print all the content of the IOregister
        """
        res = (
            utils.color.CYAN
            + f"{self.IO_type}"
            + utils.color.ENDC
            + utils.color.YELLOW
            + f" r{self.register.locator}"
            + utils.color.ENDC
            + " as "
        )
        if (
            self.attribute_type != valueType.attributeType.record
            and self.attribute_type != valueType.attributeType.externalrecord
            and self.attribute_type != valueType.attributeType_finalize.record
            and self.attribute_type
            != valueType.attributeType_finalize.externalrecord
        ):
            if self.closure:
                # closure always has constant
                res += utils.color.GREEN + f"{self.value}" + utils.color.ENDC
            else:
                try:
                    res += (
                        utils.color.GREEN
                        + f"{self.value}.{valueType.attributeType(self.attribute_type).name}"
                        + utils.color.ENDC
                    )
                except Exception:
                    try:
                        res += (
                            utils.color.GREEN
                            + f"{self.value}.{valueType.attributeType_finalize(self.attribute_type).name}"
                            + utils.color.ENDC
                        )
                    except Exception:
                        xexit()
        elif (
            self.attribute_type == valueType.attributeType.record
            or self.attribute_type == valueType.attributeType.externalrecord
        ):
            res += utils.color.GREEN + f"{self.value}.record" + utils.color.ENDC
        else:
            res += utils.color.GREEN + f"{self.value}" + utils.color.ENDC
        res += ";"
        xadd(res)

    def disassemble_IOregister(self, bytecodes):
        """Disassemble the IOregister

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.register = register(bytecodes)
        ### get valueType
        # utils.debug_aleo_output()
        if self.closure:
            self.value = valueType.read_closure_register_type(bytecodes)
        elif self.finalize:
            (
                self.attribute_type,
                self.value,
            ) = valueType.read_finalize_value_type(bytecodes)
        elif self.function:
            (
                self.attribute_type,
                self.value,
            ) = valueType.read_function_value_type(bytecodes)
