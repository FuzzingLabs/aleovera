from function import function
from record import record
from interface import interface
from mapping import mapping
from utils import xprint
from utils import xadd
from bytecodes import bytecodes
import utils


class aleodisassembler:
    def __init__(self, bytes) -> None:
        utils.tab_init()
        utils.aleo_output_init()
        self.bytecodes = bytecodes(bytes)
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
        """
        Read the version in the header
        """
        self.version = self.bytecodes.read_u16()

    def read_programID(self):
        """
        Read the programID in the header
        """
        len_name = self.bytecodes.read_u8()
        self.name = self.bytecodes.read_n(len_name).decode("utf-8")

        len_network = self.bytecodes.read_u8()
        self.network = self.bytecodes.read_n(len_network).decode("utf-8")

    def read_number_program_imports(self):
        """
        Read the number of imports in the header
        """
        self.number_imports = self.bytecodes.read_u8()

    def read_imports(self):
        """
        Read the imports in the header
        """
        for _ in range(self.number_imports):
            self.imports.append(self.read_programID)

    def read_number_components(self):
        """
        Read the number of components in the header
        """
        self.number_components = self.bytecodes.read_u16()

    def read_function(self, type):
        """Read a function

        Args:
            type (String): The type of the component (function/closure)
        """
        new_function = function(type, self.bytecodes)
        self.functions.append(new_function)

    def read_record(self):
        """
        Read the record
        """
        new_record = record(self.bytecodes)
        self.records.append(new_record)

    def read_interface(self):
        """
        Read the interface
        """
        new_interface = interface(self.bytecodes)
        self.records.append(new_interface)

    def read_mapping(self):
        """
        Read the mapping
        """
        new_mapping = mapping(self.bytecodes)
        self.mappings.append(new_mapping)

    def read_components(self):
        """
        Read the components
        """
        xadd("")
        for _ in range(self.number_components):
            type = self.bytecodes.read_u8()
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
                xadd("type does not exist : ", type)
            xadd("")

    def debug_print(self):
        xprint("version : ", self.version)
        xprint("number of imports : ", self.number_imports)
        xprint("number of components : ", self.number_components)

    def disassemble(self):
        """
        Disassemble the bytecodes
        """
        self.read_version()
        self.read_programID()
        xadd("program ", self.name + "." + self.network + ";")
        self.read_number_program_imports()
        self.read_imports()
        for imp in self.imports:
            xadd(f"import {imp}")
        self.read_number_components()
        self.read_components()
        print(utils.aleo_output)
