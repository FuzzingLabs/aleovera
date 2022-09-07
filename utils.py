def tab_init():
    global tab
    tab = 0


def xprint(*args, end="\n"):
    tab_str = "    " * tab
    print(tab_str + "".join(map(str, args)), end=end)


def read_n_bytes(bytecodes, n):
    index = bytecodes[:n]
    bytecodes = bytecodes[n:]
    return index, bytecodes


def read_identifier(component):
    len_identifier = component.bytecodes[0]
    component.bytecodes = component.bytecodes[1:]
    identifier = component.bytecodes[:len_identifier].decode("utf-8")
    component.bytecodes = component.bytecodes[len_identifier:]
    return identifier
