#!/usr/bin/env python

import xmiparser
import jinja2
import os

package_dir = os.path.dirname(__file__)
modelfile = os.path.join(package_dir, 'test', 'umlsample.zargo')
model = xmiparser.parse(modelfile)

def generateTemplateDict(xmiClass):
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

    # template dictionary 

    templateDict = dict(
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
    return templateDict

# render template
for xmiClass in model.getClasses():
    env = jinja2.Environment(loader=jinja2.PackageLoader('test','templates'),trim_blocks=True)
    template = env.get_template('cpp_class_src.jinja2')
    cpp_source = template.render(generateTemplateDict(xmiClass))
    print cpp_source
