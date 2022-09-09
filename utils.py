def tab_init():
    global tab
    tab = 0


def aleo_output_init():
    global aleo_output
    aleo_output = ""


def xadd(*args, end="\n"):
    global aleo_output
    tab_str = "    " * tab
    aleo_output = aleo_output + tab_str + "".join(map(str, args)).lower() + end


def xprint(*args, end="\n"):
    """Pretty printer

    Args:
        end (str, optional): Used in case of multiple print in the same line that does not need a newline. Defaults to "\n".
    """
    tab_str = "    " * tab
    print(tab_str + "".join(map(str, args)).lower(), end=end)

class ProgramId():
    def __init__(self, bytecodes) -> None:
        self.name = None
        self.network = None
        self.parse_program_id(bytecodes)
    
    def parse_program_id(self, bytecodes):
        len_name = bytecodes.read_u8()
        self.name = bytecodes.read_n(len_name).decode("utf-8")

        len_network = bytecodes.read_u8()
        self.network = bytecodes.read_n(len_network).decode("utf-8")

    def fmt(self):
        return f"{self.name}.{self.network}"


def read_variable_length_integer(bytecodes):
    """Read the size of a variable based on the first byte

    Args:
        bytecodes (bytecodes): bytecodes object
    Returns:
        Int: The size
    """
    flag = bytecodes.read_u8()
    if flag >= 0 and flag <= 252:
        return flag
    elif flag == 0xFD:
        bytecodes = bytecodes[2:]
        return 16
    elif flag == 0xFE:
        bytecodes = bytecodes[4:]
        return 32
    else:
        bytecodes = bytecodes[8:]
        return 64


def read_identifiers(bytecodes):
    """read n identifiers based on the first byte and returns a list of string

    Args:
        bytecodes (bytecodes): bytecodes object

    Returns:
        String: The identifiers list
    """
    number_of_string = bytecodes.read_u16()
    identifiers = []
    for _ in range(number_of_string):
        identifiers.append(read_identifier(bytecodes))
    return identifiers


def read_identifier(bytecodes):
    """read n bytes based on the first byte and returns a string

    Args:
        bytecodes (bytecodes): bytecodes object

    Returns:
        String: The identifier string
    """
    len_identifier = bytecodes.read_u8()
    identifier = bytecodes.read_n(len_identifier).decode("utf-8")
    return identifier


def read_locator(bytecodes):
    id = read_identifier(bytecodes)
    resource = read_identifier(bytecodes)
    return [id, resource]

def read_external(bytecodes):
    return [ProgramId(bytecodes), read_identifier(bytecodes)]
