# Python program to read and modify ipynb file
# it cleans all output and all input except comments

import json, sys, os, subprocess

def read_ipynb(filename: str) -> dict:
    # Opening JSON file
    with open(filename) as file:
    # returns JSON object as a dictionary
        data = json.load(file)
    return data

def write_ipynb(data: dict, filename: str) -> None:
    # Opening JSON file for write
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
    return

def clear_badge(data):
    if 'Open In Colab' in data['cells'][0]['source'][0]:
        data['cells'].pop(0)

def add_badge(data, outfilename):
    if "./" in outfilename:
        outfilename = outfilename[2:]

    first_input =     {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    f"[![Open In Colab](colab-badge.png)](https://colab.research.google.com/github/zoldbirka/colab-test-pub/blob/master/{outfilename})"
        ]
    }
    data['cells'].insert(0,first_input)



def main():
    # parancssori argumentumok kezelése
    len_argv = len(sys.argv)
    if  len_argv == 2:
        filename = sys.argv[1]
        filename_base = os.path.basename(filename)
        name, ext = os.path.splitext(filename_base)
    else:
        sys.exit('No filename given!')

# fál megnyitása
    try:
        data = read_ipynb(filename)
    except FileNotFoundError:
        sys.exit("No such file: %s"%filename)
# fájl feldolgozása
    clear_badge(data)
    add_badge(data, filename)
 
# fájl mentése 
    try:
        write_ipynb(data, filename)
    except FileNotFoundError:
        sys.exit("No such dictionary: %s"%filename)
    return 0

if __name__ == "__main__":
    main()
