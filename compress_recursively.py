#!/usr/bin/python3

import sys
import subprocess
import os
from pathlib import Path


if len(sys.argv) < 2:
    sys.stderr.write(f"Not enough parameters\nUsage: {sys.argv[0]} <path>")

dirpath = sys.argv[1]

total_size_before = os.path.getsize(dirpath)

for file in Path(dirpath).rglob("*.[pP][dD][fF]"):
    basename = os.path.basename(file)
    initial_size = int(os.path.getsize(file))
    print(f"\'{basename}\' is {initial_size} bytes long")

    subprocess.run(["ps2pdf", "-dPDFSETTINGS=/ebook", "-dSAFER", file, "temp.pdf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    final_size = int(os.path.getsize("./temp.pdf"))
    if final_size < initial_size:
        subprocess.run(["mv", "temp.pdf", file])
        total_size_after += final_size
        percentage = (final_size/initial_size) * 100
        print(f"Reduced to {final_size} bytes")
        print(f"File is now {percentage:.2f}% of its original size\n")
        continue
    print("File did not get smaller, mantaining the original one\n")

total_size_after = os.path.getsize(dirpath)

subprocess.run(["rm", "./temp.pdf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"'{dirpath}' was {total_size_before} bytes long, reduced to {final_size} bytes")
print(f"Is now {((total_size_after/total_size_before)*100):.2f}% its original size")
