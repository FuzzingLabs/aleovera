from . import utils
from enum import Enum
from .register import register
from .utils import xexit
from .valueType import LiteralType


class OperandType(Enum):
    Literal = 0
    Register = 1
    ProgramID = 2
    Caller = 3


class Literal:
    def __init__(self, bytecodes, read_value=False) -> None:
        self.type = None
        try:
            self.type = LiteralType(bytecodes.read_u16())
        except Exception as e:
            xexit()
        self.value = None
        self.has_value = read_value
        if read_value:
            self.value = self.read_literal_value(bytecodes)

    def read_literal_value(self, bytecodes):
        res = "UNHANDLED LITERAL TYPE"
        if self.type == LiteralType.I128 or self.type == LiteralType.U128:
            if self.type == LiteralType.I128:
                res = bytecodes.read_i128()
            else:
                res = bytecodes.read_u128()

        elif self.type == LiteralType.I64 or self.type == LiteralType.U64:
            if self.type == LiteralType.I64:
                res = bytecodes.read_i64()
            else:
                res = bytecodes.read_u64()

        elif self.type == LiteralType.I32 or self.type == LiteralType.U32:
            if self.type == LiteralType.I32:
                res = bytecodes.read_i32()
            else:
                res = bytecodes.read_u32()

        elif self.type == LiteralType.I16 or self.type == LiteralType.U16:
            if self.type == LiteralType.I16:
                res = bytecodes.read_i16()
            else:
                res = bytecodes.read_u16()

        elif self.type == LiteralType.I8 or self.type == LiteralType.U8:
            if self.type == LiteralType.I8:
                res = bytecodes.read_i8()
            else:
                res = bytecodes.read_u8()
        elif self.type == LiteralType.Boolean:
            res = bytecodes.read_u8()
            if res == 0:
                res = "false"
            else:
                res = "true"
        elif self.type == LiteralType.Address:
            bytecodes.read_n(32)
        elif self.type == LiteralType.Scalar:
            res = int.from_bytes(bytecodes.read_n(32), "little")
        elif self.type == LiteralType.Field:
            res = int.from_bytes(bytecodes.read_n(32), "little")
        return res

    def fmt(self):
        res = ""
        if self.has_value:
            res = f"{self.value}"
        if self.type != LiteralType.Boolean:
            res += self.type.name
        return res


class Operand:
    def __init__(self, bytecodes, read_value=False) -> None:
        self.type = None
        self.value = None
        self.get_operand(bytecodes, read_value)

    def get_operand(self, bytecodes, read_value):
        op_type = None
        try:
            op_type = OperandType(bytecodes.read_u8())
        except Exception as e:
            xexit()
        self.type = op_type

        if op_type == OperandType.Literal:
            self.value = Literal(bytecodes, read_value)
            # if read_value:
            #     self.value = self.read_literal(literal_type, bytecodes)
            #     print(f"{self.value}{literal_type.name}")
            # else:
            #     print(f"{literal_type.name}")

        elif op_type == OperandType.Register:
            self.value = register(bytecodes)

        elif op_type == OperandType.ProgramID:
            self.value = utils.read_locator(bytecodes)

        elif op_type == OperandType.Caller:
            pass

    def fmt(self, caller_name=None):
        if self.type == OperandType.Caller:
            if caller_name:
                return utils.color.BLUE + caller_name + utils.color.ENDC
            else:
                return utils.color.BLUE + "self.caller" + utils.color.ENDC

        elif self.type == OperandType.ProgramID:
            res = ""
            if self.value:
                res = self.value[0]
                if len(self.value) > 2:
                    res += f".{self.value[1]}"
            return res

        else:
            return self.value.fmt()


class Operands:
    def __init__(self, number_of_operand, bytecodes, read_value=False) -> None:
        self.operands = self.get_operands(
            number_of_operand, bytecodes, read_value
        )

    def fmt(self, function_name=None):
        res = ""
        if len(self.operands) != 0:
            res = self.operands[0].fmt(function_name)
        for operand in self.operands[1:]:
            res += f" {operand.fmt(function_name)}"
        return res

    def get_operands(self, number_of_operand, bytecodes, read_value):
        operands = []
        for _ in range(number_of_operand):
            operands.append(Operand(bytecodes, read_value))
        return operands
