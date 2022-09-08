import os
import subprocess


def build_tests():
    cwd = os.getcwd()
    subfolders = [f.path for f in os.scandir("tests") if f.is_dir()]
    for folder in subfolders:
        os.chdir(folder)
        subprocess.run("aleo build", shell=True, check=True)
        """p = subprocess.Popen(
            "python3 ../../main.py -f build/main.avm".split(" "),
            stdout=subprocess.PIPE,
        )
        out, err = p.communicate()
        print(out)
        print(err)"""
        os.chdir(cwd)


build_tests()
