from function import function
from record import record
from interface import interface


class aleodisassembler:
    def __init__(self, bytes) -> None:
        self.bytecodes = bytes
        self.version = None
        self.name = ""
        self.network = ""
        self.number_imports = None
        self.imports = []
        self.number_components = None
        self.functions = []
        self.records = []
        print("bytecodes : ", self.bytecodes)

    def read_version(self):
        self.version = int.from_bytes(self.bytecodes[:2], "little")
        self.bytecodes = self.bytecodes[2:]

    def read_programID(self):
        len_name = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        self.name = self.bytecodes[:len_name].decode("utf-8")
        self.bytecodes = self.bytecodes[len_name:]

        len_network = self.bytecodes[0]
        self.bytecodes = self.bytecodes[1:]
        self.network = self.bytecodes[:len_network].decode("utf-8")
        self.bytecodes = self.bytecodes[len_network:]

    def read_number_program_imports(self):
        self.number_imports = self.bytecodes[
            0
        ]  # int.from_bytes(self.bytecodes[0], "little")
        self.bytecodes = self.bytecodes[1:]

    def read_imports(self):
        for i in range(self.number_imports):
            self.imports.append(self.read_programID)

    def read_number_components(self):
        self.number_components = int.from_bytes(self.bytecodes[:2], "little")
        self.bytecodes = self.bytecodes[2:]

    def read_function(self, type):
        new_function = function(type=type)
        self.bytecodes = new_function.disassemble_function(self.bytecodes)
        self.functions.append(new_function)

    def read_record(self):
        new_record = record()
        self.bytecodes = new_record.disassemble_record(self.bytecodes)
        self.records.append(new_record)

    def read_interface(self):
        new_interface = interface()
        self.bytecodes = new_interface.disassemble_interface(self.bytecodes)
        self.records.append(new_interface)

    def read_components(self):
        print("")
        for i in range(self.number_components):
            type = self.bytecodes[0]
            self.bytecodes = self.bytecodes[1:]
            if type == 0:
                print(type)
            elif type == 1:
                print("---interface detected---")
                self.read_interface()
            elif type == 2:
                print("---record detected---")
                self.read_record()
            elif type == 3:
                print("---closure detected---")
                self.read_function("closure")
            elif type == 4:
                print("---function detected---")
                self.read_function("function")
            else:
                print("type does not exist : ", type)
            print("")

    def disassemble(self):
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
