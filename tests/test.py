#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from difflib import SequenceMatcher
from aleovera.disassembler import aleodisassembler


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


color = bcolors(True)


def print_diff(ref, out):
    out = out.splitlines(True)
    outlen = len(out)
    fillen = len(ref)
    i = 0
    while i < outlen and i < fillen:
        if ref[i] != out[i]:
            print(
                color.GREEN
                + f">>> Ref: Line[{i}] - Len({len(ref[i])}) : {ref[i]}"
                + color.ENDC
            )
            print(
                color.RED
                + f"<<< Out: Line[{i}] - Len({len(out[i])}) : {out[i]}"
                + color.ENDC
            )

        i += 1
    while i < outlen:
        print(
            color.RED
            + f"<<< Out: Line[{i}] - Len({len(out[i])}) : {out[i]}"
            + color.ENDC
        )
        i += 1
    while i < fillen:
        print(
            color.GREEN
            + f">>> Ref: Line[{i}] - Len({len(ref[i])}) : {ref[i]}"
            + color.ENDC
        )
        i += 1


def build_and_test(cwd, folder, diff=False):
    crash = 0
    ratio = 0
    print("-------------------", file=sys.stderr)
    print(folder, file=sys.stderr)
    os.chdir(folder)
    # subprocess.check_call("aleo build", shell=True, stdout=subprocess.DEVNULL)

    if os.path.isfile("build/main.avm"):
        content = ""
        with open("build/main.avm", "rb") as file:
            content = file.read()
        if content == "":
            pass
        aleo = aleodisassembler(content)
        aleo.disassemble()
        output = aleo.fmt()
        f = open("main.aleo")
        unparsed_lines = f.readlines()
        file_lines = []
        for line in unparsed_lines:
            if line[:2] == "//":
                continue
            file_lines.append(line.rstrip() + "\n")
        file_lines[-1] = file_lines[-1][:-1]  # Remove the last newline

        content_file = "".join(file_lines)
        f.close()
        ratio = SequenceMatcher(None, output, content_file).ratio()
        if ratio != 1 and diff:
            print_diff(file_lines, output)

        print(ratio, file=sys.stderr)
    else:
        crash = 1
        print("NO BUILD DIRECTORY", file=sys.stderr)
    os.chdir(cwd)
    return ratio, crash


def build_tests(path, diff=False):
    cwd = os.getcwd()
    subfolders = [
        f.path for f in os.scandir(path) if (f.is_dir() and f.path != "build")
    ]
    crash = 0
    total = 0
    for folder in subfolders:
        ratio, has_crashed = build_and_test(cwd, folder, diff)
        if has_crashed == 0:
            total += ratio
        else:
            crash += 1

    print("-------------------------------------------------", file=sys.stderr)
    print(f"Folder that does not build : {crash}", file=sys.stderr)
    print(f"RATIO -- {total/(len(subfolders) - crash)}", file=sys.stderr)


parser = argparse.ArgumentParser(
    description="Run tests for the aleo disassembler."
)
parser.add_argument(
    "--path",
    "-p",
    type=str,
    nargs="*",
    default=["tests"],
    help="Paths to the specific directories to run the test on",
)
parser.add_argument(
    "--diff",
    "-d",
    dest="diff",
    action="store_true",
    help="A diff-like output between output and reference",
)
parser.add_argument(
    "--recurse",
    "-r",
    dest="recurse",
    action="store_true",
    help="The path given are path to directories containing directories containing the aleo files",
)

args = parser.parse_args()

for path in args.path:
    if args.recurse:
        build_tests(path, args.diff)
    else:
        build_and_test(os.getcwd(), path, args.diff)
