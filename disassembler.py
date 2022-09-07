from function import function
from record import record
from interface import interface
from mapping import mapping
from utils import xprint
import utils


class aleodisassembler:
    def __init__(self, bytes) -> None:
        utils.tab_init()
        self.bytecodes = bytes
        self.version = None
        self.name = ""
        self.network = ""
        self.number_imports = None
        self.imports = []
        self.number_components = None
        self.functions = []
        self.records = []
        self.mappings = []

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
        self.number_imports = self.bytecodes[0]
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

    def read_mapping(self):
        new_mapping = mapping()
        self.bytecodes = new_mapping.disassemble_mapping(self.bytecodes)
        self.mappings.append(new_mapping)

    def read_components(self):
        xprint("")
        for _ in range(self.number_components):
            type = self.bytecodes[0]
            self.bytecodes = self.bytecodes[1:]
            if type == 0:
                self.read_mapping()
            elif type == 1:
                self.read_interface()
            elif type == 2:
                self.read_record()
            elif type == 3:
                self.read_function("closure")
            elif type == 4:
                self.read_function("function")
            else:
                xprint("type does not exist : ", type)
            xprint("")

    def disassemble(self):
        self.read_version()
        xprint("version : ", self.version)
        self.read_programID()
        xprint("program ID : ", self.name + "." + self.network)
        self.read_number_program_imports()
        xprint("number of imports : ", self.number_imports)
        self.read_imports()
        xprint("imports : ", self.imports)
        self.read_number_components()
        xprint("number of components : ", self.number_components)
        self.read_components()
