#! /usr/bin/python

from optparse import OptionParser
import os
import sys
import jinja2
from validators import YamlValidator, Validator


# TODO get jinja to add opts.SRCDIR as a director full of templates (see FileSystemLoader in jinja2 documenation)
# TODO create an abstract base class (see python abc class documentation) for validating, outside of this file
# TODO create a YAML validating class that inherits the baseclass, so that we can validate the generated yaml is compliant
#      you will need to add pyyaml to poetry 
# TODO add a command line argument to specify the generator (i.e yaml) so that running this can validate
#      prior to writing the file. if it fails to validate, exit 1
# TODO add a custom validator to run the circle validation tool (there is one), inheriting from the same base class
# TODO add unit tests (see python unittest library) for the generator class
# TODO read variables from a file specified in opts (i.e load a specific yaml file full of variables), 
#      use those variables in the jinja render context


if __name__ == "__main__":
    
    p = OptionParser()
    p.add_option("-s", "--src", dest="SRCDIR", action="store", help="Directory containing jinja templates")
    p.add_option("-t", "--template", dest="TEMPLATE", action="store", help="Source Template to be generated")
    p.add_option("-d", "--dest", dest="DEST", action="store", help="insert the destination for each file you want to parse")
    p.add_option("-x", "--debug", dest="DEBUG", action="store_true", help="Set, to print to the console only.")
    opts, args = p.parse_args()

    if opts.DEBUG:
        print(opts)

    if opts.TEMPLATE is None or not os.path.isfile(opts.TEMPLATE):
        sys.stderr.write("Invalid template file.\n")
        sys.exit(3)

    if opts.SRCDIR is None or not os.path.isdir(opts.SRCDIR):
        sys.stderr.write("Invalid source directory.\n")
        sys.exit(3)

    val = YamlValidator() 
    taxt = open("templates/yml.").read()       
    print(val.validate(text))

    '''
    d = {'hello': "world"}
    with open(opts.TEMPLATE, "r") as fp:
        tmpl = fp.read()

    templateLoader = jinja2.FileSystemLoader(searchpath=opts.SRCDIR)
    templateEnv = jinja2.Environment(loader=templateLoader)
    with open(opts.TEMPLATE, "r") as fp:
        TEMPLATE_FILE = fp.read()
    temp = jinja2.Template(TEMPLATE_FILE)
    
    template = templateEnv.get_template(tmpl)
    outputText = template.render(d)

    if opts.DEBUG:
        print(outputText)

    if opts.DEST is not None:
        with open(opts.DEST, "w") as fp:
            fp.write(outputText)
    '''
