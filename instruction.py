from enum import Enum, auto


class Opcode(Enum):
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


UNARY = [Opcode.Abs, Opcode.AbsWrapped, Opcode.Double, Opcode.Inv, Opcode.Neg, Opcode.Not, Opcode.Square,
        Opcode.SquareRoot, Opcode.HashBHP256, Opcode.HashBHP512, Opcode.HashBHP768, Opcode.HashBHP1024,
        Opcode.HashPED64, Opcode.HashPED128, Opcode.HashPSD2, Opcode.HashPSD4, Opcode.HashPSD8]

BINARY = [Opcode.Add, Opcode.AddWrapped, Opcode.Sub, Opcode.SubWrapped, Opcode.Mul, Opcode.MulWrapped,
        Opcode.Div, Opcode.DivWrapped, Opcode.Rem, Opcode.RemWrapped, Opcode.Pow, Opcode.PowWrapped,
        Opcode.Shl, Opcode.ShlWrapped, Opcode.Shr, Opcode.ShrWrapped, Opcode.And, Opcode.Or, Opcode.Nand,
        Opcode.Nor, Opcode.GreaterThan, Opcode.GreaterThanOrEqual, Opcode.LessThan, Opcode.LessThanOrEqual,
        Opcode.IsEq, Opcode.IsNeq, Opcode.CommitBHP256, Opcode.CommitBHP512, Opcode.CommitBHP768,
        Opcode.CommitBHP1024, Opcode.CommitPED64, Opcode.CommitPED128]

ASSERT = [Opcode.AssertEq, Opcode.AssertNeq]

class Operand(Enum):
    Literal = 0
    Register = 1
    ProgramID = 2
    Caller = 3


class Literal(Enum):
    address = (0,)
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

    """
    Seeems like there's 2 convention for storing strings, so to handle it
    we just give the number needed when its not the first case
    """
    def read_strings(self, number_of_string = 0):
        if (number_of_string == 0):
            number_of_string = int.from_bytes(self.bytecodes[:2], "little")
            self.bytecodes = self.bytecodes[2:]
        line = []
        for _ in range(number_of_string):
            size_of_string = int.from_bytes(self.bytecodes[:1], "little")
            self.bytecodes = self.bytecodes[1:]
            string = self.bytecodes[:size_of_string].decode("ascii")
            self.bytecodes = self.bytecodes[size_of_string:]
            line.append(string)
        return line

    def read_register(self):
        content_type = int.from_bytes(
            self.bytecodes[:1], "little"
        )  # 0 if immediate, 1 if its like r0.zzz.bbb ...
        self.bytecodes = self.bytecodes[1:]
        register = int.from_bytes(self.bytecodes[:1], "little")
        self.bytecodes = self.bytecodes[1:]
        line = f"r{register}"
        if content_type == 1:
            for string in self.read_strings():
                line += f'.{string}'
        return line

    # Output of an instruction can only be a register 
    def read_instruction_output(self):
        output = self.read_register()
        return output



    def get_operands(self, number_of_operand):
        operands = []
        
        for _ in range(number_of_operand):
            op_type = Operand(int.from_bytes(self.bytecodes[:1], "little"))
            self.bytecodes = self.bytecodes[1:]
            if op_type == Operand.Literal:
                literal_type = Literal(
                    int.from_bytes(self.bytecodes[:2], "little")
                )
                self.bytecodes = self.bytecodes[2:]
                value = self.read_literal(literal_type)
                operands.append("{}{}".format(value, literal_type.name))

            elif op_type == Operand.Register:
                line = self.read_register()
                operands.append(line)
            
            elif op_type == Operand.ProgramID:
                name = self.read_strings(1)[0]
                res = name
                while self.bytecodes[0] != 0:
                    tail = self.read_strings(1)[0]
                    res += f'.{tail}'
                self.bytecodes = self.bytecodes[1:] # The one from the loop
                operands.append(f"{res}")

        return operands


    def read_binary_instruction(self, opcode):
        operands = self.get_operands(2)

        output = self.read_instruction_output()

        print(f"{opcode.name} {operands[0]} {operands[1]} into {output}")

    def read_variadic_instruction(self, opcode):
        number_of_operand = int.from_bytes(self.bytecodes[:1], "little")
        self.bytecodes = self.bytecodes[1:]
        operands = ""

        for string in self.get_operands(number_of_operand):
            operands += " " + string

        # Get output register
        output = self.read_instruction_output()

        # Get casted type (Should be a single string)
        number_of_string = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        cast = self.read_strings(number_of_string)

        print(f"{opcode.name}{operands} into {output} as {cast[0]}")

    def read_cast_instruction(self):
        return self.read_variadic_instruction(Opcode.Cast)

    def read_function_instructions(self):
        index = int.from_bytes(self.bytecodes[:2], "little")
        self.bytecodes = self.bytecodes[2:]
        opcode = Opcode(index)

        # Need to make lists of function using the same pattern as xor (input1, input2, output) to dont decompile wrongly
        if opcode is Opcode.Cast:
            self.read_cast_instruction()
        elif opcode is Opcode.Call:
            print("UNTESTED - UNIMPLEMENTED")
        elif opcode is Opcode.Ternary:
            print("UNTESTED - UNIMPLEMENTED")
        elif opcode in ASSERT:
            print("UNTESTED - UNIMPLEMENTED")
        elif opcode in UNARY:
            print("UNTESTED - UNIMPLEMENTED")
        else:
            self.read_binary_instruction(opcode)

    def disassemble_instruction(self, bytes):
        self.bytecodes = bytes
        self.read_function_instructions()
        rest_of_bytecodes = self.bytecodes
        self.bytecodes = bytes[: len(bytes) - len(rest_of_bytecodes)]
        return rest_of_bytecodes
