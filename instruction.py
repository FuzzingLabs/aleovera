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

class Operand(Enum):
    Literal = 0
    Register = 1
    ProgramID = 2
    Caller = 3

class Literal(Enum):
    address = 0,
    boolean = 1
    field = 2
    group = 3
    i8 = 4
    i16 = 5
    i32 = 6
    i64 = 7
    i128 = 8
    u8 = 9
    u16 = 10
    u32 = 11
    u64 = 12
    u128 = 13
    scalar = 14
    string = 15


class instruction:
    def __init__(self) -> None:
        self.bytecodes = None

    def read_literal(self, type):
        res = "UNHANDLED LITERAL TYPE"
        if type == Literal.i128 or type == Literal.u128:
            res = int.from_bytes(self.bytecodes[:16], "little")
            self.bytecodes = self.bytecodes[16:]
                                                        
        elif type == Literal.i64 or type == Literal.u64:
            res = int.from_bytes(self.bytecodes[:8], "little")
            self.bytecodes = self.bytecodes[8:]

                
        elif type == Literal.i32 or type == Literal.u32:
            res = int.from_bytes(self.bytecodes[:4], "little")
            self.bytecodes = self.bytecodes[4:]

        elif type == Literal.i16 or type == Literal.u16:
            res = int.from_bytes(self.bytecodes[:2], "little")
            self.bytecodes = self.bytecodes[2:]
        
        elif type == Literal.i8 or type == Literal.u8:
            res = int.from_bytes(self.bytecodes[:1], "little")
            self.bytecodes = self.bytecodes[1:]
        
        return res


    def read_function_in_in_regout(self, opcode_name):
        operands = []

        print(self.bytecodes)

        for _ in range(2):
            op_type = Operand(int.from_bytes(self.bytecodes[:1], "little"))
            self.bytecodes = self.bytecodes[1:]
            if op_type == Operand.Literal:
                literal_type = Literal(int.from_bytes(self.bytecodes[:2], "little"))
                self.bytecodes = self.bytecodes[2:]
                value = self.read_literal(literal_type)
                operands.append("{}{}".format(value, literal_type.name))



            elif op_type == Operand.Register:
                self.bytecodes = self.bytecodes[1:] # Skip an unsed byte for registers
                register = int.from_bytes(self.bytecodes[:1], "little")
                operands.append("r{}".format(register))
                self.bytecodes = self.bytecodes[1:]


        unk = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]

        register = int.from_bytes(self.bytecodes[:1], "little")
        operands.append("r" + str(register))
        self.bytecodes = self.bytecodes[1:]
        print(
            f"{opcode_name} {operands[0]} {operands[1]} into {operands[2]}"
        )

    def read_function_instructions(self):
        index = int.from_bytes(self.bytecodes[:2], "little")
        self.bytecodes = self.bytecodes[2:]
        opcode_name = opcode(index).name
        
        # Need to make lists of function using the same pattern as xor (input1, input2, output) to dont decompile wrongly
        self.read_function_in_in_regout(opcode_name)


    def disassemble_instruction(self, bytes):
        self.bytecodes = bytes
        self.read_function_instructions()
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
