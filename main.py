#!/usr/bin/env python3

import argparse
import csv
import os

def get_args() -> argparse.Namespace:
    
    parser = argparse.ArgumentParser(
                prog="csv2pdf",
                description="Convert a csv file into a pdf.",
                epilog="Requires pandoc."
            )
    
    parser.add_argument("-f", "--filename", help="the csv file to convert")
    parser.add_argument("--font-size", default="8", help="the font size to use (default: 8)")
    parser.add_argument("--header", default="", help="the header text at the top of every file (default: \"\")")

    return parser.parse_args()

def get_data(filename: str) -> tuple[list, list]:
    
    with open(filename, "r") as infile:
        reader = list(csv.reader(infile, delimiter=","))

    headings = reader.pop(0)

    return headings, reader


def csv_to_md(headings: list, data: list, fontsize: int, header: str) -> str:
    
    PANDOC_HEADER = f"""\
---
geometry: margin=1in
fontsize: {fontsize}pt
header-includes: |
    \\usepackage{{fancyhdr}}
    \\pagestyle{{fancy}}
    \\fancyhead[CO,CE]{{{header}}}
    \\fancyfoot[CO,CE]{{}}
    \\fancyfoot[LE,RO]{{}}
---
"""
    
    string = PANDOC_HEADER
    
    for row in data:
        for i, value in enumerate(row):
            string += f"""
**{headings[i]}:**
{value.replace("-", "")}
"""
        string += "\\newpage"

    return string
    
if __name__ == "__main__":

    args = get_args()
    heading, data = get_data(args.filename)
    
    with open("tmp.md", "w") as outfile:
        outfile.write(csv_to_md(heading, data, args.font_size, args.header))

    os.system(f"pandoc -s -o {args.filename}.pdf tmp.md")
    os.remove("tmp.md")
