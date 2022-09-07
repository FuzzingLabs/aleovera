def tab_init():
    global tab
    tab = 0


def xprint(*args, end="\n"):
    tab_str = "    " * tab
    print(tab_str + "".join(map(str, args)), end=end)


def read_variable_length_integer(bytecodes):
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
    number_of_string = bytecodes.read_u16()
    identifiers = []
    for _ in range(number_of_string):
        identifiers.append(read_identifier(bytecodes))
    return identifiers


def read_identifier(bytecodes):
    len_identifier = bytecodes.read_u8()
    identifier = bytecodes.read_n(len_identifier).decode("utf-8")
    return identifier
