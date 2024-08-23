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

def modify_source(cells):
    if '#' in ''.join(cells['source']) and cells['source'][0][:2] != '##':
        res = []
        num = 0
        for elem in cells['source']:
            elem = elem.strip()
            if '#' in elem:
                if '#' == elem[0]:
                    res.append(elem + '\n')
                else:
                    line = elem.split('#')
                    res.append('# '+line[-1]+'\n')
                num += 1
        if num  > 0:
            res.append('')
        cells['source'] = res

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
    f"[![Open In Colab](../notebooks/colab-badge.png)](https://colab.research.google.com/github/zoldbirka/colab-test-pub/blob/master/{outfilename})"
        ]
    }
    data['cells'].insert(0,first_input)



def main():
    # parancssori argumentumok kezelése
    len_argv = len(sys.argv)
    if  1 < len_argv <= 3:
        filename = sys.argv[1]
        filename_base = os.path.basename(filename)
        name, ext = os.path.splitext(filename_base)
        outfilename = name + "_URES" + ext
        if len_argv == 3:
            outdir = sys.argv[2]
            outfilename = os.path.join(outdir, outfilename)
    else:
        sys.exit('No filename given!')

# fál megnyitása
    try:
        data = read_ipynb(filename)
    except FileNotFoundError:
        sys.exit("No such file: %s"%filename)
# fájl feldolgozása
    clear_badge(data)
    add_badge(data, outfilename)

    for cells in data['cells']:
        if cells['cell_type'] == 'code':
            modify_source(cells)
            cells['outputs'] = []    
# fájl mentése 
    try:
        write_ipynb(data, outfilename)
    except FileNotFoundError:
        sys.exit("No such dictionary: %s"%outfilename)

    conv_pdf = False
    if conv_pdf:
        convert_str = "cd ./notebooks\n"
        convert_str += f'jupyter nbconvert --to pdf {filename_base} --output ../_pdf/{name}.pdf'
        subprocess.run(convert_str, shell=True)
    return 0

if __name__ == "__main__":
    main()
