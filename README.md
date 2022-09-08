# AleoVera, the aleo bytecode analyzer and disassembler
<img src ="https://img.shields.io/badge/python-3.10-blue.svg"/>

AleoVera is an Aleo analyzer & disassembler written in Python 3. AleoVera's features also include the generation of the call graph and control-flow graph (CFG) of a given Aleo compilation artifact.

## Installation

```sh
sudo apt install graphviz

git clone https://github.com/FuzzingLabs/ALeoVera && cd AleoVera

pip install .

aleovera -h
```

## Disassemble the contract's compilation artifact (AVM)

```sh
aleo new foo
cd foo
aleo build
aleovera -f ./build/main.avm
```

# F.A.Q
## How to run the tests?

``` sh
python3 tests/test.py
```

## How to build the documentation?

```sh
# Install sphinx
apt-get install python3-sphinx

#Create the docs folder
mkdir docs & cd docs

#Init the folder
sphinx-quickstart docs

#Modify the `conf.py` file by adding
import aleovera

#Generate the .rst files before the .html files
sphinx-apidoc -f -o . ..

#Generate the .html files
make html

#Run a python http server
cd _build/html; python3 -m http.server
```


# License

AleoVera is licensed and distributed under the AGPLv3 license. [Contact us](mailto:contact@fuzzinglabs.com) if you're looking for an exception to the terms.
