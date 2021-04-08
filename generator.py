#! /usr/bin/python

from optparse import OptionParser
import os
import sys
import jinja2


if __name__ == "__main__":
    
    p = OptionParser()
    p.add_option("-s", "--src", dest="SRCDIR", action="store", help="Directory containing jinja templates")
    p.add_option("-t", "--template", dest="TEMPLATE", action="store", help="Source Template to be generated")
    p.add_option("-d", "--dest", dest="DEST", action="store", help="insert the destination for each file you want to parse")
    p.add_option("-x", "--debug", dest="DEBUG", action="store_true", help="Set, to print to the console only.")
    opts, args = p.parse_args()

    print(opts)
    if opts.TEMPLATE is None or not os.path.isfile(opts.TEMPLATE):
        sys.stderr.write("Invalid template file.\n")
        sys.exit(3)

    if opts.SRCDIR is None or not os.path.isdir(opts.SRCDIR):
        sys.stderr.write("Invalid source directory.\n")
        sys.exit(3)

    dict = {'hello': "world"}
    with open(opts.TEMPLATE, "r") as fp:
        tmpl = fp.read()

    j2 = jinja2.Template(tmpl)
    rendered = j2.render(dict)
    if opts.DEBUG:
        print(rendered)

    if opts.DEST is not None:
        with open(opts.DEST, "w") as fp:
            fp.write(rendered)