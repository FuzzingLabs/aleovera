import sys


class bytecodes:
    """
    Class containing the bytecodes of the smart contract.
    """

    def __init__(self, bytes) -> None:
        self.bytecodes = bytes

    def read_u8(self):
        """Read one byte

        Returns:
            Int: the int format of the byte
        """
        return int.from_bytes(self.read_n(1), "little")

    def read_u16(self):
        """read 2 bytes

        Returns:
            Int: the int format of the bytes
        """
        return int.from_bytes(self.read_n(2), "little")

    def read_u32(self):
        """read 4 bytes

        Returns:
            Int: the int format of the bytes
        """
        return int.from_bytes(self.read_n(4), "little")

    def read_u64(self):
        """read 8 bytes

        Returns:
            Int: the int format of the bytes
        """
        return int.from_bytes(self.read_n(8), "little")

    def read_n(self, n):
        """Read n bytes

        Args:
            n (Int): Number of bytes to read

        Returns:
            Byte: The bytes read
        """
        if n > len(self.bytecodes):
            sys.exit(f"Bytecodes length < {n}")
        res = self.bytecodes[:n]
        self.bytecodes = self.bytecodes[n:]
        return res

    def peek(self):
        """Get the first byte

        Returns:
            Byte: The byte read
        """
        return self.bytecodes[0]
