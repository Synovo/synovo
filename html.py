#!/usr/bin/python3

import sys
import argparse

from template import template


parser = argparse.ArgumentParser(description="HTML Filetype Support")

parser.add_argument('--source', metavar="source", help="The document to be templated")
parser.add_argument('--build', metavar="build", help="The directory where all build resources are stored")
parser.add_argument('--out', metavar="out", help="The complete path of the final resource")
                    
args = parser.parse_args(sys.argv[1:])

print(args)

with open(args.source, 'r') as source, open(args.out, 'w+') as dest:
    dest.write(template(source.read(), 'article', { 
        'out': args.out,
        'source': args.source,
        'build': args.build
    }, {}))
