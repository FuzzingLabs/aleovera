import os
import sys
import subprocess
import argparse
from difflib import SequenceMatcher

def print_diff(ref, out):
    out = out.split("\n")
    outlen = len(out)
    fillen = len(ref)
    i = 0
    while (i < outlen and i < fillen):
        if ref[i] != out[i]:
            print(f">>> {ref[i]}")
            print(f"<<< {out[i]}")
        i += 1
    while (i < outlen):
        print(f"<<< {out[i]}")
        i += 1
    while (i < fillen):
        print(f">>> {ref[i]}")
        i+= 1

def build_and_test(cwd, folder, diff=False):
    crash = 0
    ratio = 0
    print("-------------------", file=sys.stderr)
    print(folder, file=sys.stderr)
    os.chdir(folder)
    subprocess.check_call(
        "aleo build", shell=True, stdout=subprocess.DEVNULL
    )

    if os.path.isfile("build/main.avm"):
        a
        p = subprocess.Popen(
            "python3 -m aleovera -f build/main.avm".split(" "),
            stdout=subprocess.PIPE,
        )
        f = open("main.aleo")
        unparsed_lines = f.readlines()
        file_lines = []
        for line in unparsed_lines:
            if line[:2] == "//":
                continue
            file_lines.append(line.rstrip() + "\n")
            
        content_file = "".join(file_lines)
        f.close()
        output, _ = p.communicate()
        output = output.decode("utf-8")
        # print(output)
        # print("----")
        # print(content_file)
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
    subfolders = [f.path for f in os.scandir(path) if (f.is_dir() and f.path != "build")]
    crash = 0
    total = 0
    for folder in subfolders:
        ratio, has_crashed = build_and_test(cwd, folder, diff)
        if (has_crashed == 0):
            total += ratio
        else:
            crash += 1

    print("-------------------------------------------------", file=sys.stderr)
    print(f"Folder that does not build : {crash}", file=sys.stderr)
    print(f"RATIO -- {total/(len(subfolders) - crash)}", file=sys.stderr)



parser = argparse.ArgumentParser(description='Run tests for the aleo disassembler.')
parser.add_argument('--path', '-p', type=str, nargs='*', default=["tests"],
                    help='Paths to the specific directories to run the test on')
parser.add_argument('--diff', '-d',dest='diff', action="store_true",
                    help='A diff-like output between output and reference')
parser.add_argument('--recurse', '-r',dest='recurse', action="store_true",
                    help='The path given are path to directories containing directories containing the aleo files')

args = parser.parse_args()

for path in args.path:
    if args.recurse:
        build_tests(path, args.diff)
    else:
        build_and_test(os.getcwd(), path, args.diff)
