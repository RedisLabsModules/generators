#! /usr/bin/python

from optparse import OptionParser
import os
import sys
import importlib
import jinja2
import validators


# TODO get jinja to add opts.SRCDIR as a director full of templates (see FileSystemLoader in jinja2 documenation)
# TODO create a YAML validating class that inherits the baseclass, so that we can validate the generated yaml is compliant
#      you will need to add pyyaml to poetry 
# TODO add a custom validator to run the circle validation tool (there is one), inheriting from the same base class
# TODO add unit tests (see python unittest library) for the generator class
# TODO read variables from a file specified in opts (i.e load a specific yaml file full of variables), 
#      use those variables in the jinja render context

### ------ DONE 
# create an abstract base class (see python abc class documentation) for validating, outside of this file
# add a command line argument to specify the generator (i.e yaml) so that running this can validate
#      prior to writing the file. if it fails to validate, exit 1


if __name__ == "__main__":
    
    p = OptionParser()
    p.add_option("-s", "--src", dest="SRCDIR", help="Directory containing jinja templates")
    p.add_option("-t", "--template", dest="TEMPLATE", help="Source Template to be generated")
    p.add_option("-d", "--dest", dest="DEST", help="insert the destination for each file you want to parse")
    p.add_option("-x", "--debug", dest="DEBUG", action="store_true", help="Set, to print to the console only.")
    p.add_option("-v", "--validator", dest="VALIDATOR", help="The validator to run.")
    opts, args = p.parse_args()

    if opts.DEBUG:
        print(opts)

    if opts.TEMPLATE is None or not os.path.isfile(opts.TEMPLATE):
        sys.stderr.write("Invalid template file.\n")
        sys.exit(3)

    if opts.SRCDIR is None or not os.path.isdir(opts.SRCDIR):
        sys.stderr.write("Invalid source directory.\n")
        sys.exit(3)

    if opts.VALIDATOR is not None and opts.VALIDATOR not in validators.VALIDATORS:
        sys.stderr.write("%s is not one of %s.\n" % (opts.VALIDATOR, validators.VALIDATORS))
        sys.exit(1)


    d = {'hello': "world"}
    # with open(opts.TEMPLATE, "r") as fp:
    #     tmpl = fp.read()

    searchpath = os.path.dirname(os.path.abspath(opts.TEMPLATE))
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(loader=templateLoader)
    tmpl = templateLoader.load(name=opts.TEMPLATE, environment=templateEnv)
    content = tmpl.render(d)

    valid = True
    if opts.VALIDATOR is not None:
        v = validators.Validator()
        valid = v.validate(opts.VALIDATOR, content)

    if valid:
        if opts.DEBUG:
            print(content)

        if opts.DEST is not None:
            with open(opts.DEST, "w") as fp:
                fp.write(content)