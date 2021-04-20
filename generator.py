import os
import yaml
import sys
import jinja2
import validators
from validators import create_validator


# TODO use python type hints for functions and change the function signatures
# TODO add a custom validator to run the circle validation tool (there is one), inheriting from the same base class
#    https://circleci.com/docs/2.0/local-cli/#manual-download
# TODO add to the command line, the ability to pass in variables ex:
#  python generator.py <-- whatever we use> -var FOO=bar -var something=12345
#     FEEL FREE TO CHANGE THIS SYNTAX TO ANYTHING THAT IS EASY TO PROGRAM

class Generator(object):

    def __init__(self, template, debug=False):
        """ // SAMPLE REMOVE ME
        kwargs['TEMPLATE'] - A string containing a path to a template to generate.
        """
        self.TEMPLATE = template
        self.DEBUG = debug

        # Check that the template file is valid.
        if self.TEMPLATE is None or not os.path.isfile(self.TEMPLATE):
            err = "Invalid template file.\n"
            raise AttributeError(err)

    def __read_varfile__(self, fname):
        """This function generates the variables dictionary if the VARIABLES option was marked."""
        with open(fname) as fp:
            return yaml.load(fp, Loader=yaml.SafeLoader)

    def generate(self, srcpath=None, varfile=None, validator=None, dest=None):
        """Generate the content from the template file. If a filename is provided, this will write to disk
        in addition to returning the content."""
        
        # If the source file was given - Check that the source dir is valid
        if srcpath is not None and not os.path.isdir(srcpath):
            err = "Invalid source directory.\n"
            raise AttributeError(err)

        # If the variables file was given - Check that it's a file.
        if varfile is not None and not os.path.isfile(varfile):
            err = "Invalid source file for variables.\n"
            raise AttributeError(err)

        # If the validator was given - Check that validators support this kind of validation.
        if validator is not None and validator not in validators.VALIDATORS:
            err = "%s is not one of %s.\n" % (validator, validators.VALIDATORS)
            raise AttributeError(err)

        # If the variables file was given - read it's content
        self.VARS = {}
        if varfile is not None:
            self.VARS = self.__read_varfile__(varfile)
            if self.VARS is None:
                err = "You can't give an empty file as a variable file.\n"
                raise AttributeError(err)
            if self.DEBUG:
                print(self.VARS)

        # Render the template
        searchpath = [os.path.abspath(os.path.dirname(self.TEMPLATE)), ]
        if srcpath is not None:
            searchpath.append(os.path.abspath(srcpath))
        templateLoader = jinja2.FileSystemLoader(searchpath)
        templateEnv = jinja2.Environment(loader=templateLoader)
        tmpl = templateLoader.load(name=os.path.basename(self.TEMPLATE), environment=templateEnv)
        content = tmpl.render(self.VARS)
        if self.DEBUG:
            print(content)

        # If the validator was given - create the corresponding validator and validate
        if validator is not None:
            v = create_validator(validator)
            if not v.is_valid(content):
                err = "The content that was generated is not a valid %s file.\n" % (validator)
                raise Exception(err)

        # if the dest file was given - write the rendered content to the file
        if dest is not None:
            with open(dest, "w+") as fp:
                fp.write(content)

        return content


if __name__ == "__main__":
    from optparse import OptionParser

    p = OptionParser()
    p.add_option("-s", "--src", dest="SRCDIR", help="Directory containing jinja templates")
    p.add_option("-t", "--template", dest="TEMPLATE", help="[REQUIRED] Source Template to be generated")
    p.add_option("-d", "--dest", dest="DEST", help="Insert the destination parsed file")
    p.add_option("-x", "--debug", dest="DEBUG", action="store_true", help="Set, to print to the console only.")
    p.add_option("-c", "--validator", dest="VALIDATOR", help="The validator to run.")
    p.add_option("-v", "--variables", dest="VARIABLES", help="Read variables from yaml file.")
    opts, args = p.parse_args()

    g = Generator(opts.TEMPLATE, opts.DEBUG)
    g.generate(opts.SRCDIR, opts.VARIABLES, opts.VALIDATOR, opts.DEST)
