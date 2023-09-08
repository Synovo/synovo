#!/usr/bin/python3

import sys
import argparse
from markdown_it import MarkdownIt

from template import template


parser = argparse.ArgumentParser(description="DocX Filetype Support")

parser.add_argument('--source', metavar="source", help="The document to be templated")
parser.add_argument('--build', metavar="build", help="The directory where all build resources are stored")
parser.add_argument('--out', metavar="out", help="The complete path of the final resource")
                    
args = parser.parse_args(sys.argv[1:])

print(args)

md = (
    MarkdownIt('commonmark', {'breaks':True,'html':True})
    .enable('table')
)


with open(args.source, 'r') as source, open(args.out, 'w+') as dest:
    dest.write(template(md.render(source.read()), 'article', { 
        'out': args.out,
        'source': args.source,
        'build': args.build
    }, {}))
