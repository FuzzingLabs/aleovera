from aleovera.disassembler import aleodisassembler
import glob
import os


def disassembler_coverage():
    all_test = glob.glob("./*/build/main.avm")
    for test in all_test:
        print(test)
        with open(test, "rb") as file:
            content = file.read()
            filename = os.path.basename(file.name).split(".")[0]
            disassembler = aleodisassembler(content, color=True)
            disassembler.disassemble()
            disassembler.print_disassembly()
            disassembler.print_call_flow_graph(filename, "pdf")


disassembler_coverage()
