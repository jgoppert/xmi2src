#!/usr/bin/python

from lxml import etree
import jinja2
import os


class CppGenerator:

    def __init__(self,modelFile,outputPath="generated_code"):
        schema = etree.XMLSchema(file="mda.xsd")
        parser = etree.XMLParser(dtd_validation=False, schema=schema)
        root = etree.parse(modelFile,parser)
        for classObject in root.findall("class"):
            templateDict = self.processClass(classObject)
            template = jinja2.Template(open("templates/cpp_class_src.jinja2").read());
            code = template.render(templateDict)
            if not os.path.exists(outputPath):
                os.mkdir(outputPath)
            f = open("generated_code/"+templateDict["name"]+".hpp","w")
            f.write(code)
            f.close()
            print code

    def processClass(self,classObject):

        # name
        name = classObject.find("name").text
        if name == None:
            raise IOError("class name not found")
        
        # doc
        doc = classObject.find("doc").text
        if doc == None:
            doc = ""

        return dict(name=name,doc=doc)

if __name__ == "__main__":
    CppGenerator("apo.xml")
