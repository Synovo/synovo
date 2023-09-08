#!/usr/bin/python3

import os
import sys
import shutil
from pathlib import Path
import argparse
import subprocess


default_generator = [
    ["docx", "./docx.py"],
    ["md", "./md.py"]
]


parser = argparse.ArgumentParser(description="Website Builder")

parser.add_argument("--pages", "-p", default=["./pages"], action="append", metavar="dir", help="The root directory of all pages")
parser.add_argument("--language", default=["en"], action="append", metavar="lang", help="Which languages should be exported. If a document does not exist in a given language, a blank document with an error message and a link to the english version is generated instead.")
parser.add_argument("--static", "-s", default=[["./static", "./static"]], nargs=2, metavar=("static", 'dest'), action="append", help="Add static resources to the website")
parser.add_argument("--out", "-o", default="./build", metavar="build", action="store", help="Where should the final static site be placed")
parser.add_argument("--generator", "-g", nargs=2, metavar=("extension", "script"), action="append", default=default_generator, help="How should files of a certain extension be compiled into the website. The second argument should be a script or command-line")

args = parser.parse_args(sys.argv[1:])

codes = []

for i in args.pages:
    for root, dirs, files in os.walk(os.path.abspath(i)):
        for file, path in [(file, os.path.join(root, file)) for file in files]:
            split = file.split('.')
            matcher = split[-1]
            lang = split[-2]

            if lang in args.language:
                script = next((x for x in args.generator if x[0] == split[-1]), None)

                if not script:
                    print("No matcher defined for", split[-1], "- Skipping")
                    continue
                
                out = os.path.abspath(os.path.join(args.out, lang, Path(path).relative_to(os.path.abspath(i)).parent, '.'.join(split[:-2] + ['html'])))
                proc = subprocess.run([os.path.abspath(script[1]), '--source', path, '--out', out, '--build', os.path.abspath(args.out)])
                codes.append(proc.returncode)

for i in args.static:
    root_src_dir = os.path.abspath(i[0])
    root_dst_dir = os.path.abspath(os.path.join(args.out, i[1]))

    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


if len([i for i in codes if not i == 0]):
    print("A process didn't exist properly")
    sys.exit(1)
else:
    print("Rebuilt")
