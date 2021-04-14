import os
import sys
import jinja2
import validators


# TODO add a custom validator to run the circle validation tool (there is one), inheriting from the same base class
# TODO add unit tests (see python unittest library) for the generator class


### ------ DONE 
# get jinja to add opts.SRCDIR as a director full of templates (see FileSystemLoader in jinja2 documenation)
# create an abstract base class (see python abc class documentation) for validating, outside of this file
# add a command line argument to specify the generator (i.e yaml) so that running this can validate
#      prior to writing the file. if it fails to validate, exit 1
# create a YAML validating class that inherits the baseclass, so that we can validate the generated yaml is compliant
#      you will need to add pyyaml to poetry 
# read variables from a file specified in opts (i.e load a specific yaml file full of variables), 
#      use those variables in the jinja render context

class Generator(object):

    def __init__(self, args, opts):
        self.ARGS = args
        self.OPTS = opts
        self.__check_input_validity__()
        
        self.VALID = True
        self.CONTENT = ""
        self.DICT = self.__generate_dict__(self.OPTS.VARIABLES)


    def __check_input_validity__(self):
        '''
        This function validate that all the givan variables in opts dictionary
        is valid.
        '''

        if self.OPTS.DEBUG:
            print(self.OPTS, self.ARGS)

        # Check if the template file was given and that it's a valid file.
        if self.OPTS.TEMPLATE is None or not os.path.isfile(self.OPTS.TEMPLATE):
            sys.stderr.write("Invalid template file.\n")
            sys.exit(3)

        # If the source file was given - Check that the source dir is valid
        if self.OPTS.SRCDIR is not None and not os.path.isdir(self.OPTS.SRCDIR):
            sys.stderr.write("Invalid source directory.\n")
            sys.exit(3)

        # If the variables file was given - Check that it's a file.
        if self.OPTS.VARIABLES is not None and not os.path.isfile(self.OPTS.VARIABLES):
            sys.stderr.write("Invalid source file for variables.\n")
            sys.exit(3)

        # If the validate option was choosen - Check that validators support this kind of validation.
        if self.OPTS.VALIDATOR is not None and self.OPTS.VALIDATOR not in validators.VALIDATORS:
            sys.stderr.write("%s is not one of %s.\n" % (self.OPTS.VALIDATOR, validators.VALIDATORS))
            sys.exit(1)
    
    def __generate_dict__(self, file_name):
        '''
        This function generates the variables dictipnary if the VARIABLES option was marked.
        '''
        d = dict()
        if file_name is not None:
            with open(file_name) as f: 
                d = eval(f.read())

        if self.OPTS.DEBUG: 
            print(d)

        return d

    def __create_tamplate_and_render__(self):
        '''
        This creates the template loader and the template environment for jinja rendering
        and returns the rendered content.
        '''

        searchpath = [os.path.dirname(os.path.abspath(self.OPTS.TEMPLATE))]
        if self.OPTS.SRCDIR is not None:
            searchpath.append(os.path.abspath(self.OPTS.SRCDIR))
        templateLoader = jinja2.FileSystemLoader(searchpath)
        templateEnv = jinja2.Environment(loader=templateLoader)
        tmpl = templateLoader.load(name=self.OPTS.TEMPLATE, environment=templateEnv)
        content = tmpl.render(self.DICT)

        return content

    def __validate__(self, content):
        is_valid = True

        if self.OPTS.VALIDATOR is not None:
            v = validators.Validator()
            is_valid =  v.validate(self.OPTS.VALIDATOR, content)

        if not is_valid:
            sys.stderr.write("Sometring went wrong. The content is not valid.\nTo see the content run in debug mode (-x).")
            if self.OPTS.DEBUG:
                sys.stderr.write("Content: %s \n" % (self.CONTENT))
            sys.exit(1)

        return is_valid

    def generate_file(self):

        self.CONTENT = self.__create_tamplate_and_render__()
        self.VALID = self.__validate__(self.CONTENT)
  
        if self.OPTS.DEBUG:
            print(self.CONTENT)

        if self.OPTS.DEST is not None:
            with open(self.OPTS.DEST, "w") as fp:
                fp.write(self.CONTENT)   
