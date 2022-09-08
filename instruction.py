from enum import Enum, auto
import bytecodes
from register import register
from IOregister import IOregister
import valueType
import utils
from operand import Operands, Operand, OperandType


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


UNARY = [
    Opcode.Abs,
    Opcode.AbsWrapped,
    Opcode.Double,
    Opcode.Inv,
    Opcode.Neg,
    Opcode.Not,
    Opcode.Square,
    Opcode.SquareRoot,
    Opcode.HashBHP256,
    Opcode.HashBHP512,
    Opcode.HashBHP768,
    Opcode.HashBHP1024,
    Opcode.HashPED64,
    Opcode.HashPED128,
    Opcode.HashPSD2,
    Opcode.HashPSD4,
    Opcode.HashPSD8,
]

BINARY = [
    Opcode.Add,
    Opcode.AddWrapped,
    Opcode.Sub,
    Opcode.SubWrapped,
    Opcode.Mul,
    Opcode.MulWrapped,
    Opcode.Div,
    Opcode.DivWrapped,
    Opcode.Rem,
    Opcode.RemWrapped,
    Opcode.Pow,
    Opcode.PowWrapped,
    Opcode.Shl,
    Opcode.ShlWrapped,
    Opcode.Shr,
    Opcode.ShrWrapped,
    Opcode.And,
    Opcode.Xor,
    Opcode.Or,
    Opcode.Nand,
    Opcode.Nor,
    Opcode.GreaterThan,
    Opcode.GreaterThanOrEqual,
    Opcode.LessThan,
    Opcode.LessThanOrEqual,
    Opcode.IsEq,
    Opcode.IsNeq,
    Opcode.CommitBHP256,
    Opcode.CommitBHP512,
    Opcode.CommitBHP768,
    Opcode.CommitBHP1024,
    Opcode.CommitPED64,
    Opcode.CommitPED128,
]

ASSERT = [Opcode.AssertEq, Opcode.AssertNeq]


class instruction:
    """
    The instruction class
    """

    def __init__(self) -> None:
        self.bytecodes = None
        self.opcode = None
        self.operands = None
        self.output = None
        self.cast = None

    def fmt(self):
        """Get the disassembly of the opcode

        Returns:
            String: The disassembly of the opcode
        """
        if self.opcode is Opcode.Cast:
            # The output register of the cast is not of a register type
            return (
                f"Cast {self.operands.fmt()} into r{self.output} as {self.cast}"
            )
        elif self.opcode is Opcode.Call:
            self.disass = "UNTESTED - UNIMPLEMENTED"
        elif self.opcode is Opcode.Ternary:
            self.disass = "UNTESTED - UNIMPLEMENTED"
        elif self.opcode in ASSERT:
            self.disass = "UNTESTED - UNIMPLEMENTED"
        elif self.opcode in UNARY:
            return f"{self.opcode.name} {self.operands.fmt()} into {self.output.fmt()}"
        elif self.opcode in BINARY:
            return f"{self.opcode.name} {self.operands.fmt()} into {self.output.fmt()}"
        else:
            self.disass = "UNKNOWN opcode"

    def read_identifier(self):
        size_of_string = int.from_bytes(self.bytecodes[:1], "little")
        self.bytecodes = self.bytecodes[1:]
        string = self.bytecodes[:size_of_string].decode("ascii")
        self.bytecodes = self.bytecodes[size_of_string:]
        return string

    """
    Seeems like there's 2 convention for storing strings, so to handle it
    we just give the number needed when its not the first case
    """

    def read_identifiers(self, number_of_string=0):
        if number_of_string == 0:
            number_of_string = int.from_bytes(self.bytecodes[:2], "little")
            self.bytecodes = self.bytecodes[2:]
        line = []
        for _ in range(number_of_string):
            line.append(self.read_identifier())
        return line

    """
impl<N: Network> FromBytes for PlaintextType<N> {
    /// Reads a plaintext type from a buffer.
    fn read_le<R: Read>(mut reader: R) -> IoResult<Self> {
        let variant = u8::read_le(&mut reader)?;
        match variant {
            0 => Ok(Self::Literal(LiteralType::read_le(&mut reader)?)),
            1 => Ok(Self::Interface(Identifier::read_le(&mut reader)?)),
            2.. => Err(error(format!("Failed to deserialize annotation variant {variant}"))),
        }
    }
}
    """

    def read_plaintext(self):
        variant = int.from_bytes(self.bytecodes[:1], "little")
        if variant == 0:
            return self.bytecodes[:2].decode("ascii")
        elif variant == 1:
            return self.read_identifier()
        else:
            return f"Failed to deserialize {variant}"

    def read_register_type(self):
        variant = int.from_bytes(self.bytecodes[:1], "little")
        self.bytecodes = self.bytecodes[1:]
        if variant == 0:
            self.read_plaintext()
        elif variant == 1:
            print()
        elif variant == 2:
            print()
        else:
            print("INVALID REGISTER TYPE")

    # Decode the value of a variable length integer.
    # https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer

    def read_variable_length_integer(self):
        flag = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        if flag >= 0 and flag <= 252:
            return flag
        elif flag == 0xFD:
            self.bytecodes = self.bytecodes[2:]
            return 16
        elif flag == 0xFD:
            self.bytecodes = self.bytecodes[4:]
            return 32
        else:
            self.bytecodes = self.bytecodes[8:]
            return 64

    # def read_register2(self, bytecodes):
    #     variant = int.from_bytes(
    #         self.bytecodes[:1], "little"
    #     )  # 0 if immediate, 1 if its like r0.zzz.bbb ...
    #     self.bytecodes = self.bytecodes[1:]
    #     locator = self.read_variable_length_integer()
    #     if variant == 0:
    #         return f'r{locator}'
    #     elif variant == 1:
    #         return self.read_identifiers()
    #     return "Invalid"

    def read_binary_instruction(self, bytecodes):
        """Read binary instruction

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.operands = Operands(2, bytecodes, True)
        self.output = register(bytecodes)

    def read_unary_instruction(self, bytecodes):
        """Read unary instruction

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.operands = Operands(1, bytecodes, True)
        self.output = register(bytecodes)

    def read_cast_instruction(self, bytecodes):
        """Read CAST instruction

        Args:
            bytecodes (bytecodes): The bytecodes object

        Returns:
            String: Return a string containing an error
        """
        number_of_operand = bytecodes.read_u8()

        if number_of_operand == 0 or number_of_operand > 8:
            print(f"Invalid cast ({number_of_operand} parameters)")

        self.operands = Operands(number_of_operand, bytecodes, True)

        # Get output register, its formatted like an IO register
        if bytecodes.read_u8() != 0:
            return "Error in cast"

        self.output = bytecodes.read_u8()

        # Get casted type (Should be a single string) but stored weirdly, need to improve
        valtype = bytecodes.peek()
        self.cast = "ERROR PARSING CAST TYPE"
        if valtype == 0:
            bytecodes.read_u8()
            self.cast = valueType.read_plaintext(bytecodes)
        elif valtype == 1:
            self.cast = valueType.read_plaintext(bytecodes)

    def disassemble_instruction(self, bytecodes):
        """Disassemble the instruction

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        index = bytecodes.read_u16()
        self.opcode = Opcode(index)
        # Need to make lists of function using the same pattern as xor (input1, input2, output) to dont decompile wrongly
        if self.opcode is Opcode.Cast:
            self.read_cast_instruction(bytecodes)
        elif self.opcode is Opcode.Call:
            self.disass = "UNTESTED - UNIMPLEMENTED"
        elif self.opcode is Opcode.Ternary:
            self.disass = "UNTESTED - UNIMPLEMENTED"
        elif self.opcode in ASSERT:
            self.disass = "UNTESTED - UNIMPLEMENTED"
        elif self.opcode in UNARY:
            self.read_unary_instruction(bytecodes)
        elif self.opcode in BINARY:
            self.read_binary_instruction(bytecodes)
        else:
            self.disass = "UNKNOWN opcode"
