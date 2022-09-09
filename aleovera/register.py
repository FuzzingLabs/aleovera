from . import utils


class register:
    """
    The register class
    """

    def __init__(self, bytecodes) -> None:
        self.locator = None
        self.identifiers = None
        self.disassemble_register(bytecodes)

    def disassemble_register(self, bytecodes):
        """Disassemble the register

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        variant = (
            bytecodes.read_u8()
        )  # 0 if immediate, 1 if its like r0.zzz.bbb ...
        self.locator = utils.read_variable_length_integer(bytecodes)
        if variant == 1:
            self.identifiers = utils.read_identifiers(bytecodes)

    def fmt(self):
        """Get the register

        Returns:
            String: The register with its locator
        """
        res = f"r{self.locator}"
        if self.identifiers != None:
            for identifier in self.identifiers:
                res += f".{identifier}"
        return res
