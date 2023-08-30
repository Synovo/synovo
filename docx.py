#!/usr/bin/python3

import subprocess
import tempfile
import pathlib
import sys
import os

from template import template

tmp_fd, tmp_path = tempfile.mkstemp()

subprocess.run(['pandoc', '--from', 'docx', '--to', 'html', '--embed-resources', '--reference-doc', './reference.docx', '--section-divs'], stdin=open(sys.argv[1]), stdout=tmp_fd)

os.makedirs(pathlib.Path(sys.argv[2]).parent, exist_ok=True)

with open(sys.argv[2], 'w+') as out:
    out.write(template(tmp_path))
