import utils
import bytecodes


class register:
    def __init__(self, bytecodes) -> None:
        self.locator = None
        self.identifier = None
        self.disassemble_register(bytecodes)

    def disassemble_register(self, bytecodes):
        variant = (
            bytecodes.read_u8()
        )  # 0 if immediate, 1 if its like r0.zzz.bbb ...
        self.locator = utils.read_variable_length_integer(bytecodes)
        if variant == 1:
            self.identifier = utils.read_identifiers(bytecodes)
