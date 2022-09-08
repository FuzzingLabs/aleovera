import os
import subprocess
from difflib import SequenceMatcher


def build_tests():
    cwd = os.getcwd()
    subfolders = [f.path for f in os.scandir("tests") if f.is_dir()]
    for folder in subfolders:
        os.chdir(folder)
        subprocess.run("aleo build", shell=True, check=True)
        if os.path.isdir("build/"):
            p = subprocess.Popen(
                "python3 ../../main.py -f build/main.avm".split(" "),
                stdout=subprocess.PIPE,
            )
            f = open("main.aleo")
            content_file = f.readlines()
            content_file = "".join(content_file)
            f.close()
            output, err = p.communicate()
            output = output.decode("utf-8")
            # print(output)
            # print("----")
            # print(content_file)
            ratio = SequenceMatcher(None, output, content_file).ratio()
            print(ratio)
        else:
            print("NO BUILD DIRECTORY")
        os.chdir(cwd)


build_tests()
