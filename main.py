from disassembler import aleodisassembler
import argparse
import os


def parse_args():
    """Parse the program arguments
    Returns:
        list: list containing arguments
    """
    parser = argparse.ArgumentParser(
        add_help=True,
        description="Aleo Disassembler",
        epilog="The exit status is 0 for non-failures and -1 for failures.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    c = parser.add_argument_group("mandatory arguments")
    c.add_argument(
        "-f",
        "-file",
        "--file",
        metavar="file",
        type=argparse.FileType("rb"),
        nargs="+",
        required=True,
        help="AVM file",
    )
    m = parser.add_argument_group("optional arguments")
    m.add_argument(
        "-c",
        "-call",
        "--call",
        action="store_true",
        help="Print call flow graph",
    )
    m.add_argument(
        "-format",
        "--format",
        metavar="Format of the output file [png-svg-pdf]",
        nargs="?",
        choices=["pdf", "png", "svg"],
        help="Format of the graphs",
    )
    return parser.parse_args()


def aleovera():
    args = parse_args()
    with args.file[0] as f:
        aleo = aleodisassembler(f.read())
    aleo.disassemble()
    aleo.print_disassembly()
    filename = os.path.basename(args.file[0].name).split(".")[0]
    format = "pdf" if args.format is None else str(args.format)
    if args.call:
        aleo.print_call_flow_graph(filename=filename, format=format)


if __name__ == "__main__":
    aleovera()
