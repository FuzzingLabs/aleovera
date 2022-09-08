import utils
from enum import Enum, auto
from register import register

class OperandType(Enum):
    Literal = 0
    Register = 1
    ProgramID = 2
    Caller = 3


class LiteralType(Enum):
    address = 0
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

class Literal:
    def __init__(self, bytecodes, read_value=False) -> None:
        self.type = LiteralType(bytecodes.read_u16())
        self.value = None
        if (read_value):
            self.value = self.read_literal_value(bytecodes)
        
    def read_literal_value(self, bytecodes):
        res = "UNHANDLED LITERAL TYPE"
        if self.type == LiteralType.i128 or self.type == LiteralType.u128:
            res = bytecodes.read_u128()

        elif self.type == LiteralType.i64 or self.type == LiteralType.u64:
            res = bytecodes.read_u64()

        elif self.type == LiteralType.i32 or self.type == LiteralType.u32:
            res = bytecodes.read_u32()

        elif self.type == LiteralType.i16 or self.type == LiteralType.u16:
            res = bytecodes.read_u16()

        elif self.type == LiteralType.i8 or self.type == LiteralType.u8:
            res = bytecodes.read_u8()

        return res

    def fmt(self):
        res = ""
        if (self.value):
            res = f"{self.value}"
        res += self.type.name
        return res

class Operand:
    def __init__(self, bytecodes, read_value=False) -> None:
        self.type = None
        self.value = None
        self.get_operand(bytecodes, read_value)

    def get_operand(self, bytecodes, read_value):
        op_type = OperandType(bytecodes.read_u8())
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
            # operands.append(reg.fmt())
            
        elif op_type == OperandType.ProgramID:
            name = utils.read_identifier(bytecodes)
            network = utils.read_identifier(bytecodes)
            self.value = [name, network]
            # operands.append(f'{name}.{network}')

        elif op_type == OperandType.Caller:
            pass
    
    def fmt(self, caller_name=None):
        if self.type == OperandType.Caller:
            if caller_name:
                return caller_name
            else:
                return "self.caller"
        
        elif self.type == OperandType.ProgramID:
            res = ""
            if self.value:
                res = self.value[0]
                if len(self.value) > 1:
                    res += f'.{self.value[1]}'
            return res

        else:
            return self.value.fmt()


class Operands:
    def __init__(self, number_of_operand, bytecodes, read_value=False) -> None:
        self.operands = self.get_operands(number_of_operand, bytecodes, read_value)

    def fmt(self):
        res = ""
        if len(self.operands) != 0:
            res = self.operands[0].fmt()
        for operand in self.operands[1:]:
            res += f" {operand.fmt()}"
        return res



    def get_operands(self, number_of_operand, bytecodes, read_value):
        operands = []
        for _ in range(number_of_operand):
            operands.append(Operand(bytecodes, read_value))
        return operands