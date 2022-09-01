from enum import Enum, auto
from disassembler import aleodisassembler


def main():
    f = open("test/build/main.avm", "rb")
    aleo = aleodisassembler(f.read())
    aleo.disassemble()


main()
