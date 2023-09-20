# encoder.py
# Author: Ethan Coleman
import os
from PIL import Image
import pickle

FRAME_DIR = "C:\\Dev\\LED_Cube\\Frame Sets\\"
PATTERN_DIR = "C:\\Dev\\LED_Cube\\output\\pattern.h"
TIMING_DIR = "C:\\Dev\\LED_Cube\\output\\timing.p"
BASE_MAIN_DIR = "C:\\Dev\\LED_Cube\\base\\Led_Cube_base.h"
MAIN_DIR = "C:\\Dev\\LED_Cube\\output\\Led_Cube.h"

def add_pattern(name, timing_set):
    dirpath = FRAME_DIR + name
    paths = os.listdir(dirpath)

    im = Image.open(os.path.join(dirpath, paths[len(paths) - 1]), 'r')
    pix = im.load()
    pix = [pix[i % 8, i // 8] for i in range(0, 64)]
    bits = [val[3] for val in pix]

    prev_swaps = list()
    for i in range(0, 64):
        if (bits[i] == 255):
            r = (i % 32) // 8
            c = (i % 8) % 4
            p = (2 * (i // 32)) + ((i % 8) // 4)
            prev_swaps.append(r*16+c*4+p)

    tot = 0
    initial = len(prev_swaps)
    initial_swaps = [item for item in prev_swaps]
    frame_list = list()
    for n, path in enumerate(paths):
        im = Image.open(os.path.join(dirpath, path), 'r')
        pix = im.load()
        pix = [pix[i % 8, i // 8] for i in range(0, 64)]
        bits = [val[3] for val in pix]

        swaps = list()
        for i in range(0, 64):
            if (bits[i] == 255):
                r = (i % 32) // 8
                c = (i % 8) % 4
                p = (2 * (i // 32)) + ((i % 8) // 4)
                swaps.append(r*16+c*4+p)
        nexts = [item for item in swaps]
        for swap in prev_swaps:
            if not(swap in swaps):
                swaps.append(swap)
            else:
                swaps.remove(swap)
        prev_swaps = nexts

        tot += len(swaps) + 2
        frame_list.append(f"\t{timing_set[n]}, {len(swaps)}, {', '.join(map(str, swaps))},\n")

    with open(PATTERN_DIR, 'r') as base_file:
        base = base_file.read().split("|||||")
    with open(PATTERN_DIR, 'w') as out:
        out.write(base[0] + "\n")
        out.write(f"unsigned char {name}[] =\n")
        out.write("{\n")
        out.write(f"\t{tot // 256}, {tot % 256}, {initial}," + "\n") 
        if(initial > 0): out.write("\t" + ", ".join(map(str,initial_swaps)) + "," + "\n")
        out.writelines(frame_list)
        out.write("};\n|||||")

def clear_spacer():
    with open(PATTERN_DIR, 'r') as base_file:
        base = base_file.read().split("|||||")
    with open(PATTERN_DIR, 'w') as out:
        out.write(base[0])

def clear_patterns():
    with open(PATTERN_DIR, 'w') as out:
        out.write("/* Patterns.h\n * Author: Ethan Coleman\n*/\n\n// Pattern data")

def add_switch(name_list : list[str]):
    write_name = lambda name: " ".join([nm[0] + nm[1:].lower() for nm in name.split("_")])
    with open(BASE_MAIN_DIR, 'r') as base_file:
        base = base_file.read().split("|||||")
    with open(MAIN_DIR, 'w') as out:
        out.write(base[0] + str(len(name_list) - 1))
        out.write(base[1])
        for i, name in enumerate(name_list):
            out.write(f"\t\t\tcase {i}:\n")
            out.write(f"\t\t\t\tInitialize_Mode({name});\n")
            param = write_name(name) + (" " * (16 - len(write_name(name))))
            out.write(f"\t\t\t\tLCD.print(\"{param}\");\n")
            out.write(f"\t\t\t\tbreak;")
            if i < len(name_list) - 1:
                out.write("\n")
        out.write(base[2])

def add_all_patterns(use_timing = True):
    timings = pickle.load(open(TIMING_DIR, "rb"))
    names = os.listdir(FRAME_DIR)
    clear_patterns()
    for i, name in enumerate(names):
        if (use_timing):
            add_pattern(name, timings[i])
        else:
            add_pattern(name, [0] * len(timings[i]))
    clear_spacer()

if __name__ == "__main__":
    add_switch(os.listdir(FRAME_DIR))
    add_all_patterns(use_timing = True)