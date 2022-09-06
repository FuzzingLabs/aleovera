from dis import Bytecode
from enum import Enum, auto


class opcode(Enum):
    Abs = 0
    AbsWrapped = auto()
    Add = auto()
    AddWrapped = auto()
    And = auto()
    AssertEq = auto()
    AssertNeq = auto()
    Call = auto()
    Cast = auto()
    CommitBHP256 = auto()
    CommitBHP512 = auto()
    CommitBHP768 = auto()
    CommitBHP1024 = auto()
    CommitPED64 = auto()
    CommitPED128 = auto()
    Div = auto()
    DivWrapped = auto()
    Double = auto()
    GreaterThan = auto()
    GreaterThanOrEqual = auto()
    HashBHP256 = auto()
    HashBHP512 = auto()
    HashBHP768 = auto()
    HashBHP1024 = auto()
    HashPED64 = auto()
    HashPED128 = auto()
    HashPSD2 = auto()
    HashPSD4 = auto()
    HashPSD8 = auto()
    Inv = auto()
    IsEq = auto()
    IsNeq = auto()
    LessThan = auto()
    LessThanOrEqual = auto()
    Modulo = auto()
    Mul = auto()
    MulWrapped = auto()
    Nand = auto()
    Neg = auto()
    Nor = auto()
    Not = auto()
    Or = auto()
    Pow = auto()
    PowWrapped = auto()
    Rem = auto()
    RemWrapped = auto()
    Shl = auto()
    ShlWrapped = auto()
    Shr = auto()
    ShrWrapped = auto()
    Square = auto()
    SquareRoot = auto()
    Sub = auto()
    SubWrapped = auto()
    Ternary = auto()
    Xor = auto()


class instruction:
    def __init__(self) -> None:
        self.bytecodes = None

    def read_function_regin_regin_regout(self, opcode_name):
        operands = []

        for _ in range(2):
            op_type = int.from_bytes(self.bytecodes[:2], "little")
            self.bytecodes = self.bytecodes[2:]
            if op_type != 1:
                print(f"TODO opcode handling for opcode: {opcode_name}")
            else:
                operands.append(self.bytecodes[0])
                self.bytecodes = self.bytecodes[1:]
        unk = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]

        operands.append(self.bytecodes[0])
        self.bytecodes = self.bytecodes[1:]
        print(
            f"{opcode_name} r{operands[0]} r{operands[1]} into r{operands[2]}"
        )

    def read_function_instructions(self):
        index = int.from_bytes(self.bytecodes[:2], "little")
        self.bytecodes = self.bytecodes[2:]
        opcode_name = opcode(index).name
        
        # Need to make lists of function using the same pattern as xor (input1, input2, output) to dont decompile wrongly
        self.read_function_regin_regin_regout(opcode_name)


    def disassemble_instruction(self, bytes):
        self.bytecodes = bytes
        self.read_function_instructions()
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
