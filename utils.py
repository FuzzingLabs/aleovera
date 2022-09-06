def read_n_bytes(bytecodes, n):
    index = bytecodes[:n]
    bytecodes = bytecodes[n:]
    return index, bytecodes
