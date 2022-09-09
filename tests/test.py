import os
import sys
import subprocess
from difflib import SequenceMatcher


def build_tests():
    cwd = os.getcwd()
    subfolders = [f.path for f in os.scandir("tests") if f.is_dir()]
    crash = 0
    total = 0
    for folder in subfolders:
        print("-------------------", file=sys.stderr)
        print(folder, file=sys.stderr)
        os.chdir(folder)
        subprocess.check_call(
            "aleo build", shell=True, stdout=subprocess.DEVNULL
        )

        if os.path.isfile("build/main.avm"):
            p = subprocess.Popen(
                "python3 ../../main.py -f build/main.avm".split(" "),
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
            if ratio != 1 and len(sys.argv) == 2 and sys.argv[1] == "-d":
                output_lines = output.split("\n")
                outlen = len(output_lines)
                fillen = len(file_lines)
                i = 0
                while (i < outlen and i < fillen):
                    if file_lines[i] != output_lines[i]:
                        print(f">>> {file_lines[i]}")
                        print(f"<<< {output_lines[i]}")
                    i += 1
                while (i < outlen):
                    print(f"<<< {output_lines[i]}")
                    i += 1
                while (i < fillen):
                    print(f">>> {file_lines[i]}")
                    i+= 1

            print(ratio, file=sys.stderr)
            total += ratio
        else:
            crash += 1
            print("NO BUILD DIRECTORY", file=sys.stderr)
        os.chdir(cwd)
    print("-------------------------------------------------", file=sys.stderr)
    print(f"Folder that does not build : {crash}", file=sys.stderr)
    print(f"RATIO -- {total/(len(subfolders) - crash)}", file=sys.stderr)


build_tests()
