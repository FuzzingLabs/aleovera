import traceback
import sys
import os

# Graphical stuff for the CallFlowGraph's dot
CALLGRAPH_CONFIG = {
    "default": {
        "shape": "oval",
        "color": "",
        "style": "solid",
        "fillcolor": "white",
    },
    "entrypoint": {"shape": "doubleoctagon", "style": "filled"},
    "import": {"style": "filled", "fillcolor": "lightcoral"},
    "constructor": {"style": "filled", "fillcolor": "violet"},
    "l1_handler": {"style": "filled", "fillcolor": "lightskyblue"},
    "external": {"style": "filled", "fillcolor": "lightgreen"},
    "view": {"style": "filled", "fillcolor": "orange"},
    "raw_input": {"style": "filled", "fillcolor": "salmon"},
    "raw_output": {"style": "filled", "fillcolor": "tomato"},
    "known_ap_change": {"style": "filled", "fillcolor": "yellow"},
}
CALLGRAPH_NODE_ATTR = {
    "style": "filled",
    "shape": "rect, plaintext",
    "pencolor": "#00000044",
    "fontname": "Helvetica,Arial,sans-serif",
}
CALLGRAPH_GRAPH_ATTR = {
    "fontname": "Helvetica,Arial,sans-serif",
    "fontsize": "20",
    "layout": "dot",
    "rankdir": "LR",
    "newrank": "true",
}
CALLGRAPH_EDGE_ATTR = {
    "arrowsize": "0.5",
    "fontname": "Helvetica,Arial,sans-serif",
    "labeldistance": "3",
    "labelfontcolor": "#00000080",
    "penwidth": "2",
}


class bcolors:
    def __init__(self, color=False):
        self.HEADER = "\033[95m" if color else ""
        self.BLUE = "\033[94m" if color else ""
        self.CYAN = "\033[96m" if color else ""
        self.GREEN = "\033[92m" if color else ""
        self.YELLOW = "\033[93m" if color else ""
        self.RED = "\033[91m" if color else ""
        self.ENDC = "\033[0m" if color else ""
        self.BOLD = "\033[1m" if color else ""
        self.BEIGE = "\033[36m" if color else ""
        self.UNDERLINE = "\033[4m" if color else ""


def color_init(activate):
    global color
    color = bcolors(color=activate)


def tab_init():
    global tab
    tab = 0


def aleo_output_init():
    global aleo_output
    aleo_output = ""


def debug_aleo_output():
    print(aleo_output)


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


def xexit(error=""):
    if error == "":
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    else:
        print(error)
    sys.exit()


class ProgramId:
    def __init__(self, bytecodes) -> None:
        self.name = None
        self.network = None
        self.parse_program_id(bytecodes)

    def parse_program_id(self, bytecodes):
        len_name = bytecodes.read_u8()
        try:
            self.name = bytecodes.read_n(len_name).decode("utf-8")
        except UnicodeDecodeError:
            xexit()

        len_network = bytecodes.read_u8()
        try:
            self.network = bytecodes.read_n(len_network).decode("utf-8")
        except UnicodeDecodeError:
            xexit()

    def fmt(self):
        return color.HEADER + f"{self.name}.{self.network}" + color.ENDC


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
        flag = bytecodes.read_u16()
        return flag
    elif flag == 0xFE:
        flag = bytecodes.read_u32()
        return flag
    else:
        flag = bytecodes.read_u64()
        return flag


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
    try:
        return bytecodes.read_n(len_identifier).decode("utf-8")
    except Exception as e:
        xexit()


def read_locator(bytecodes):
    id = read_identifier(bytecodes)
    resource = read_identifier(bytecodes)
    return [id, resource]


def read_external(bytecodes):
    return [ProgramId(bytecodes), read_identifier(bytecodes)]
