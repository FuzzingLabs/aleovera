from disassembler import aleodisassembler
import argparse


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
    return parser.parse_args()


def aleovera():
    args = parse_args()
    with args.file[0] as f:
        aleo = aleodisassembler(f.read())
        aleo.disassemble()


if __name__ == "__main__":
    aleovera()
