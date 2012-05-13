#!/usr/bin/env python

import xmiparser
import jinja2
import os
import optparse

class XMI2Src():

    def __init__(self,fileName,language):
        languageTemplatePath = os.path.join('templates',language)
        self.env = jinja2.Environment(loader=jinja2.PackageLoader('xmi2src',languageTemplatePath),trim_blocks=True)
        model = xmiparser.parse(fileName)
        for xmiClass in model.getClasses():
            source = self.generateClass(xmiClass)
            print source

    def generateClass(self,xmiClass):
        name = xmiClass.getName()
        doc = xmiClass.getDocumentation()

        class VisStruct():
            def __init__(self):
                self.public = ''
                self.private = ''
                self.protected = ''

        def addBasedOnVisibility(var,varDef,allVars):
            if var.getVisibility() == 'public':
                allVars.public +=  varDef
            elif var.getVisibility() == 'private':
                allVars.private +=  varDef
            elif var.getVisibility() == 'private':
                allVars.protected +=  varDef
            else:
                IOError('unknown visibility', var.getVisibility(), 'for',var.getName())
            return allVars
        
        # attributes
        attributes = VisStruct();
        for attribute in xmiClass.getAttributeDefs():
            attributeDef = '    ' + attribute.getType() + ' ' + attribute.getName() + ';\n'
            addBasedOnVisibility(attribute,attributeDef,attributes)

        # methods
        methods = VisStruct();
        for method in xmiClass.getMethodDefs():
            print 'method', method.getName()
            for param in method.getParams():
                print 'param', param.getName()
            methodsDef = '    ' + method.getType() + ' ' + method.getName() + ';\n'
            addBasedOnVisibility(method,methodDef,methods)

        # associations
        associations = VisStruct();

        # class template dictionary 
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

    if language != 'cpp':
        parser.error('unsuppored language, only cpp currently supported')

    XMI2Src(fileName,language)

