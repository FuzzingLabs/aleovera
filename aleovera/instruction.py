from enum import Enum, auto
from .register import register
from . import valueType
from . import utils
from .operand import Operands
from .utils import xexit


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
    Mod = auto()
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
    Opcode.Mod,
]

ASSERT = [Opcode.AssertEq, Opcode.AssertNeq]
IS_CHECK = [Opcode.IsEq, Opcode.IsNeq]


class instruction:
    """
    The instruction class
    """

    def __init__(self) -> None:
        self.opcode = None
        self.operands = None
        self.output = None
        self.cast = None
        self.callee = None
        self.variant = None

    def fmt(self):
        """Get the disassembly of the instruction

        Returns:
            String: The disassembly of the instruction
        """
        # If is sorted by from smallest array to the biggest
        if self.opcode is Opcode.Cast:
            endline = ""
            if self.variant == 1 and not utils.check_interface_name(self.cast):
                endline = ".record"
            # The output register of the cast is not of a register type
            return (
                utils.color.RED
                + f"cast"
                + utils.color.ENDC
                + f" {self.operands.fmt()} into r{self.output} as {self.cast}{endline};"
            )

        elif self.opcode is Opcode.Call:
            callee = ""
            if self.variant == 1:
                callee = self.callee
            else:
                callee = f"{self.callee[0].fmt()}/{self.callee[1]}"

            output = ""
            for reg in self.output:
                output += f"{reg.fmt()} "
            output = output[:-1]

            return (
                utils.color.RED
                + f"call"
                + utils.color.ENDC
                + f" {callee} {self.operands.fmt()} into {output};"
            )

        elif self.opcode in ASSERT:
            if self.opcode is Opcode.AssertEq:
                return (
                    utils.color.RED
                    + f"assert.eq"
                    + utils.color.ENDC
                    + f" {self.operands.fmt()};"
                )
            else:
                return (
                    utils.color.RED
                    + f"assert.neq"
                    + utils.color.ENDC
                    + f" {self.operands.fmt()};"
                )

        elif self.opcode in IS_CHECK:
            if self.opcode is Opcode.IsEq:
                return (
                    utils.color.RED
                    + f"is.eq"
                    + utils.color.ENDC
                    + f" {self.operands.fmt()} into {self.output.fmt()};"
                )
            else:
                return (
                    utils.color.RED
                    + f"is.neq"
                    + utils.color.ENDC
                    + f" {self.operands.fmt()} into {self.output.fmt()};"
                )

        elif (
            self.opcode is Opcode.Ternary
            or self.opcode in UNARY
            or self.opcode in BINARY
        ):
            op = self.opcode.name

            if self.opcode.name[-7:] == "Wrapped":
                op = f"{self.opcode.name[:-7]}.w"

            elif self.opcode in [Opcode.GreaterThan, Opcode.GreaterThanOrEqual]:
                op = "gt"
                if self.opcode == Opcode.GreaterThanOrEqual:
                    op += "e"

            elif self.opcode in [Opcode.LessThan, Opcode.LessThanOrEqual]:
                op = "lt"
                if self.opcode == Opcode.LessThanOrEqual:
                    op += "e"

            elif self.opcode.name[:4] == "Hash":
                op = f"{self.opcode.name[:4]}.{self.opcode.name[4:]}"

            elif self.opcode.name[:6] == "Commit":
                op = f"{self.opcode.name[:6]}.{self.opcode.name[6:]}"

            elif self.opcode == Opcode.SquareRoot:
                op = "sqrt"
            op = utils.color.RED + op + utils.color.ENDC
            return f"{op} {self.operands.fmt()} into {self.output.fmt()};"

        else:
            self.disass = "UNKNOWN opcode"

    def read_ternary_instruction(self, bytecodes):
        """Read ternary instruction

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.operands = Operands(3, bytecodes, True)
        self.output = register(bytecodes)

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
        self.variant = valtype
        if valtype == 0:
            bytecodes.read_u8()
            self.cast = valueType.read_plaintext(bytecodes)
        elif valtype == 1:
            self.cast = valueType.read_plaintext(bytecodes)

    def read_call_instruction(self, bytecodes):
        variant = bytecodes.read_u8()
        if variant == 1:
            self.callee = utils.read_identifier(bytecodes)
        else:
            self.callee = utils.read_external(bytecodes)

        self.variant = variant

        number_of_operand = bytecodes.read_u8()
        self.operands = Operands(number_of_operand, bytecodes, True)

        # Call can have multiple output
        number_of_output = bytecodes.read_u8()

        self.output = []
        for _ in range(number_of_output):
            # Only parsing if it's a base-register
            # register = base-register *( "." identifier )
            # base-register = %"r" numeral
            # variant = bytecodes.read_u8()
            self.output.append(register(bytecodes))

    def read_assert_instruction(self, bytecodes):
        """Read assert instruction

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        self.operands = Operands(2, bytecodes, True)

    def disassemble_instruction(self, bytecodes):
        """Disassemble the instruction

        Args:
            bytecodes (bytecodes): The bytecodes object
        """
        index = bytecodes.read_u16()
        # utils.debug_aleo_output()
        try:
            # print(index)
            self.opcode = Opcode(index)
        except Exception as e:
            xexit()
        # Need to make lists of function using the same pattern as xor (input1, input2, output) to dont decompile wrongly
        if self.opcode is Opcode.Cast:
            self.read_cast_instruction(bytecodes)
        elif self.opcode is Opcode.Call:
            self.read_call_instruction(bytecodes)
        elif self.opcode is Opcode.Ternary:
            self.read_ternary_instruction(bytecodes)
        elif self.opcode in ASSERT:
            self.read_assert_instruction(bytecodes)
        elif self.opcode in UNARY:
            self.read_unary_instruction(bytecodes)
        elif self.opcode in BINARY:
            self.read_binary_instruction(bytecodes)
        else:
            self.disass = "UNKNOWN opcode"
