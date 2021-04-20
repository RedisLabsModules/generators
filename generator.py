import os
import yaml
import sys
import jinja2
import validators


# TODO add a custom validator to run the circle validation tool (there is one), inheriting from the same base class
# TODO add unit tests (see python unittest library) for the generator class
# TODO Generator class should accept **kwargs, and document the items in the dictionary
# -

class Generator(object):

    def __init__(self, opts):
        """ // SAMPLE REMOVE ME
        kwargs['TEMPLATE'] - A string containing a path to a template to generate.
        """
        self.OPTS = opts
        
        if self.OPTS.DEBUG:
            print(self.OPTS, self.ARGS)

        # Check if the template file was given and that it's a valid file.
        if self.OPTS.TEMPLATE is None or not os.path.isfile(self.OPTS.TEMPLATE):
            err = "Invalid template file.\n"
            raise AttributeError(err)

        # If the source file was given - Check that the source dir is valid
        if self.OPTS.SRCDIR is not None and not os.path.isdir(self.OPTS.SRCDIR):
            err = "Invalid source directory.\n"
            raise AttributeError(err)

        # If the variables file was given - Check that it's a file.
        if self.OPTS.VARIABLES is not None and not os.path.isfile(self.OPTS.VARIABLES):
            err = "Invalid source file for variables.\n"
            raise AttributeError(err)

        # If the validate option was choosen - Check that validators support this kind of validation.
        if self.OPTS.VALIDATOR is not None and self.OPTS.VALIDATOR not in validators.VALIDATORS:
            err = "%s is not one of %s.\n" % (self.OPTS.VALIDATOR, validators.VALIDATORS)
            raise AttributeError(err)
    
        if self.OPTS.VARIABLES:
            self.VARS = self.__read_varfile__(self.OPTS.VARIABLES)

            if self.OPTS.DEBUG: 
                print(self.VARS)

    def __read_varfile__(self, fname):
        '''
        This function generates the variables dictionary if the VARIABLES option was marked.
        '''
        with open(fname) as fp:
            return yaml.load(fp, Loader=yaml.SafeLoader)

    def generate(self, fname=None):
        '''
        Generate our content from a template file. If a filename is provided, this will write to disk
        in addition to returning the content.
        '''

        searchpath = [os.path.abspath(os.path.dirname(self.OPTS.TEMPLATE)), ]
        if self.OPTS.SRCDIR is not None:
            searchpath.append(os.path.abspath(self.OPTS.SRCDIR))
        templateLoader = jinja2.FileSystemLoader(searchpath)
        templateEnv = jinja2.Environment(loader=templateLoader)
        tmpl = templateLoader.load(name=os.path.basename(self.OPTS.TEMPLATE), environment=templateEnv)
        content = tmpl.render(self.VARS)

        if fname is not None:
            with open(fname, "w+") as fp:
                fp.write(content)

        return content

    # def __validate__(self, content):
    #     is_valid = True

    #     if self.OPTS.VALIDATOR is not None:
    #         v = validators.Validator()
    #         is_valid =  v.validate(self.OPTS.VALIDATOR, content)

    #     if not is_valid:
    #         sys.stderr.write("Sometring went wrong. The content is not valid.\nTo see the content run in debug mode (-x).")
    #         if self.OPTS.DEBUG:
    #             sys.stderr.write("Content: %s \n" % (self.CONTENT))
    #         sys.exit(1)

    #     return is_valid


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

    # g = Generator(**opts.__dict__)
    g = Generator(opts)
    try:
        g.generate_file()
    except AttributeError:
        sys.exit(3)