def tab_init():
    global tab
    tab = 0


def xprint(*args, end="\n"):
    """Pretty printer

    Args:
        end (str, optional): Used in case of multiple print in the same line that does not need a newline. Defaults to "\n".
    """
    tab_str = "    " * tab
    print(tab_str + "".join(map(str, args)).lower(), end=end)


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
    elif flag == 0xFD:
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
