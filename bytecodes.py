import sys


class bytecodes:
    def __init__(self, bytes) -> None:
        self.bytecodes = bytes

    def read_u8(self):
        return int.from_bytes(self.read_n(1), "little")

    def read_u16(self):
        return int.from_bytes(self.read_n(2), "little")

    def read_u32(self):
        return int.from_bytes(self.read_n(4), "little")

    def read_u64(self):
        return int.from_bytes(self.read_n(8), "little")

    def read_n(self, n):
        if n > len(self.bytecodes):
            sys.exit(f"Bytecodes length < {n}")
        res = self.bytecodes[:n]
        self.bytecodes = self.bytecodes[n:]
        return res
