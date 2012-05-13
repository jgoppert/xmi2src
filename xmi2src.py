#!/usr/bin/env python

import optparse
import xmiparser
import jinja2
import os

class XMI2Src(object):
    """
    This is the main xmi2src processing class. It converts XMI format
    files that are produced by UML etc. into source files in various 
    languages. Jinja2 templates are used to aid in the source code
    generation. An attempt should be made in development to keep all
    language specific processing in the template files. This will 
    simplify addition of new langagues through the addition of a 
    new Jinja2 template folder, typically found in the lang folder.
    """
    def __init__(self,fileName,language):
        """
        A contructor that takes fileName (the filename of the xmi to convert). And
        the language to convert to. Languages are specified using jinja2 templates and
        can be found in the lang folder.
        """
        languageTemplatePath = os.path.join('lang',language)
        self.env = jinja2.Environment(loader=jinja2.PackageLoader('xmi2src',languageTemplatePath),trim_blocks=True)
        model = xmiparser.parse(fileName)
        for xmiClass in model.getClasses():
            source = self.generateClass(xmiClass)
            print source

    class VisStruct():
        """
        A structure to hold, public, private, and protected attributes/functions etc.
        This allows sorting of the methods during creation with the help of the
        addBasedOnVisibility function.
        """

        def __init__(self):
            self.public = ''
            self.private = ''
            self.protected = ''

    def addBasedOnVisibility(self,var,varDef,allVars):
        """
        Based on the visibility of var, the variable definition varDef is added
        to the corresponding visibility of the allVars variable.
        """
        if var.getVisibility() == 'public':
            allVars.public +=  varDef
        elif var.getVisibility() == 'private':
            allVars.private +=  varDef
        elif var.getVisibility() == 'private':
            allVars.protected +=  varDef
        else:
            IOError('unknown visibility', var.getVisibility(), 'for',var.getName())
        return allVars

    def generateMethod(self,xmiMethod):
        """
        Generates a src method, given an XMIMethod. A dictionary is 
        created and this dictionary is used by the method template.
        """
        # generate method dictionary
        #for param in xmiMethod.getParams():
            #print 'param', param.getName()
        name = xmiMethod.getName()
        doc = xmiMethod.getDocumentation()
        type = xmiMethod.getType()
        methodTemplateDict = dict(
            name = name,
            doc = doc,
            type = type
        )

        # render method
        methodTemplate= self.env.get_template('method.jinja2')
        return methodTemplate.render(methodTemplateDict)

    def generateAttribute(self,xmiAttribute):
        """
        Generates a src attribute, given an XMIAttribute. A dictionary is 
        created and this dictionary is used by the method template.
        """
        # generate attribute dictionary
        name = xmiAttribute.getName()
        doc = xmiAttribute.getDocumentation()
        type = xmiAttribute.getType()
        attributeTemplateDict = dict(
            name = name,
            doc = doc,
            type = type
        )

        # render method
        attributeTemplate= self.env.get_template('attribute.jinja2')
        return attributeTemplate.render(attributeTemplateDict)

    def generateAssociation(self,xmiAssociation):
        """
        Generates a src association, given an XMIAssociation. A dictionary is 
        created and this dictionary is used by the method template.
        """
        # generate association dictionary
        name = xmiAssociation.getName()
        doc = xmiAssociation.getDocumentation()
        type = xmiAssociation.getType()
        associationTemplateDict = dict(
            name = name,
            doc = doc,
            type = type
        )

        # render method
        associationTemplate= self.env.get_template('association.jinja2')
        return associationTemplate.render(associationTemplateDict)

    def generateClass(self,xmiClass):
        """
        Generates a src class, given an XMIClass. A dictionary is 
        created and this dictionary is used by the method template.
        """
        # generate class dictionary
        name = xmiClass.getName()
        doc = xmiClass.getDocumentation()

        #   attributes
        attributes = self.VisStruct();
        for attribute in xmiClass.getAttributeDefs():
            self.addBasedOnVisibility(attribute,
                self.generateAttribute(attribute),attributes)

        #   methods
        methods = self.VisStruct();
        for method in xmiClass.getMethodDefs():
            self.addBasedOnVisibility(method,self.generateMethod(method),methods)

        #   associations
        associations = self.VisStruct();
        for association in xmiClass.getFromAssociations():
            self.addBasedOnVisibility(association,
                self.generateAssociation(association),associations)

        #   class template dictionary 
        classTemplateDict = dict(
            name = name,
            doc = doc,

            publicAttributes = attributes.public,
            privateAttributes = attributes.private,
            protectedAttributes = attributes.protected,

            publicMethods = methods.public,
            privateMethods = methods.private,
            protectedMethods = methods.protected,

            publicAssociations = associations.public,
            privateAssociations = associations.private,
            protectedAssociations = associations.protected,
        )

        # render class
        classTemplate = self.env.get_template('class.jinja2')
        return classTemplate.render(classTemplateDict)

# command line parsing
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f','--file',dest='fileName',help='XMI file',metavar='XMI_FILE')
    parser.add_option('-l','--language',dest='language',help='language to generate,  supported: cpp',metavar='LANGUAGE')
    (options, args) = parser.parse_args()
    fileName = options.fileName
    language = options.language

    if fileName == None:
        parser.error('must specify xmi file, -f XMI_FILE')
    elif language == None:
        parser.error('must specify language, -l LANGUAGE')

    if not os.path.exists(os.path.join('lang',language)):
        parser.error('unsuppored language, add templates to lang folder to add support')

    XMI2Src(fileName,language)
