from enum import Enum, auto
import numbers


class valueType(Enum):
    constant = 0
    public = 1
    private = 2
    record = 3
    externalrecord = 4


class instruction(Enum):
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


class input:
    def __init__(self) -> None:
        self.register_variant = None
        self.register_locator = None
        self.identifiers = []
        self.valueType = None
        self.valueType_literal = None
        self.valueType_identifier = None
        self.valueType_content = None


class function:
    def __init__(self) -> None:
        self.identifier = None
        self.number_inputs = None
        self.inputs = []
        self.number_instructions = None
        self.instructions = []


class aleobytes:
    def __init__(self, bytes) -> None:
        self.content = bytes
        self.version = None
        self.name = ""
        self.network = "None"
        self.number_imports = None
        self.imports = []
        self.number_components = None
        print("bytes start")
        print(self.content)
        print("end\n")

    def read_version(self):
        self.version = int.from_bytes(self.content[:2], "little")
        self.content = self.content[2:]

    def read_programID(self):
        len_name = self.content[0]
        self.content = self.content[1:]
        self.name = self.content[:len_name].decode("utf-8")
        self.content = self.content[len_name:]

        len_network = self.content[0]
        self.content = self.content[1:]
        self.network = self.content[:len_network].decode("utf-8")
        self.content = self.content[len_network:]

    def read_number_program_imports(self):
        self.number_imports = self.content[
            0
        ]  # int.from_bytes(self.content[0], "little")
        self.content = self.content[1:]

    def read_imports(self):
        for i in range(self.number_imports):
            self.imports.append(self.read_programID)

    def read_number_components(self):
        self.number_components = int.from_bytes(self.content[:2], "little")
        self.content = self.content[2:]

    def read_function_identifier(self):
        len_identifier = self.content[0]
        self.content = self.content[1:]
        identifier = self.content[:len_identifier].decode("utf-8")
        self.content = self.content[len_identifier:]
        return identifier

    def read_function_number_inputs(self):
        number_inputs = int.from_bytes(self.content[:2], "little")
        self.content = self.content[2:]
        return number_inputs

    def read_variable_length_integer(self):
        flag = self.content[0]
        self.content = self.content[1:]
        if flag >= 0 and flag <= 252:
            return flag
        elif flag == 0xFD:
            self.content = self.content[2:]
            return 16
        elif flag == 0xFD:
            self.content = self.content[4:]
            return 32
        else:
            self.content = self.content[8:]
            return 64

    def read_plaintext_literal(self):
        res = self.content[:2]
        self.content = self.content[2:]
        return res

    def read_plaintext_identifier(self):
        res = self.content[0]
        self.content = self.content[1:]
        return res

    def read_valueType_plaintext(self, input):
        variant = self.content[0]
        self.content = self.content[1:]
        if variant == 0:
            input.valueType_literal = self.read_plaintext_literal()
        elif variant == 1:
            input.valueType_identifier = self.read_plaintext_identifier()

    def read_value_type(self, input):
        input.valueType = self.content[0]
        self.content = self.content[1:]
        if input.valueType == 0:
            self.read_valueType_plaintext(input)
        elif input.valueType == 1:
            self.read_valueType_plaintext(input)
        elif input.valueType == 2:
            self.read_valueType_plaintext(input)
        elif input.valueType == 3:
            print("record value type todo")
        elif input.valueType == 4:
            print("external record value type todo")
        else:
            print("fail ")

    def read_function_inputs(self):
        # print(self.content)
        new_input = input()
        new_input.register_variant = self.content[0]
        self.content = self.content[1:]
        new_input.register_locator = self.read_variable_length_integer()
        if new_input.register_variant == 1:
            num_identifiers = int.from_bytes(self.content[:2], "little")
            self.content = self.content[2:]
            for i in range(num_identifiers):
                new_input.identifiers.append(self.content[0])
                self.content = self.content[1:]
        elif new_input.register_variant != 0:
            print("error register_variant")
        ### get valueTYpe
        self.read_value_type(new_input)
        print(
            f"input r{new_input.register_variant} as u{str(new_input.register_locator)}.{valueType(new_input.valueType).name}"
        )
        # print(new_input.identifiers)
        return new_input

    def read_function_number_instructions(self):
        res = int.from_bytes(self.content[:4], "little")
        self.content = self.content[4:]
        return res

    def read_function_instructions(self):
        index = int.from_bytes(self.content[:2], "little")
        self.content = self.content[2:]
        opcode = instruction(index)
        print(opcode)
        print(self.content)

    def add_function(self):
        func = function()
        func.identifier = self.read_function_identifier()
        print("func name : ", func.identifier)
        func.number_inputs = self.read_function_number_inputs()
        print("number of inputs : ", func.number_inputs)
        print("---Inputs detected---")
        for i in range(func.number_inputs):
            func.inputs.append(self.read_function_inputs())
        func.number_instructions = self.read_function_number_instructions()
        for i in range(func.number_instructions):
            self.read_function_instructions()

    def read_components(self):
        for i in range(self.number_components):
            type = self.content[0]
            self.content = self.content[1:]
            if type == 0:
                print(type)
            elif type == 1:
                print(type)
            elif type == 2:
                print(type)
            elif type == 3:
                print(type)
            elif type == 4:
                print(" ---function detected---")
                self.add_function()
            else:
                print("type does not exist : ", type)

    def read_le(self):
        self.read_version()
        print("version : ", self.version)
        self.read_programID()
        print("program ID : ", self.name + "." + self.network)
        self.read_number_program_imports()
        print("number of imports : ", self.number_imports)
        self.read_imports()
        print("imports : ", self.imports)
        self.read_number_components()
        print("number of components : ", self.number_components)
        self.read_components()


def main():
    f = open("test/build/main.avm", "rb")
    aleo = aleobytes(f.read())
    aleo.read_le()


main()
