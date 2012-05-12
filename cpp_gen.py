#!/usr/bin/python

from lxml import etree
import jinja2
import os

class CppGenerator:

    def __init__(self,modelFile,outputPath="generated_code"):

        self.schema = etree.XMLSchema(file="mda.xsd")
        self.parser = etree.XMLParser(dtd_validation=False, schema=self.schema)
        self.root = etree.parse(modelFile,self.parser)
        self.modelFile = modelFile
        self.outputPath = outputPath

        for classObject in self.root.findall("class"):
            templateDict = self.processClass(classObject)

    def processClass(self,classObject):

        # name
        name = classObject.find("name").text
        if name == None:
            raise IOError("class name not found")
        
        # doc
        doc = classObject.find("doc").text
        if doc == None:
            doc = ""

        # generate dictionary
        templateDict = dict(name=name,doc=doc)

        # generate cpp source
        template = jinja2.Template(open("templates/cpp_class_src.jinja2").read());
        code = template.render(templateDict)
        if not os.path.exists(self.outputPath):
            os.mkdir(outputPath)
        f = open("generated_code/"+templateDict["name"]+".hpp","w")
        f.write(code)
        f.close()

        # find all links involving this class
        links = self.root.findall("link")
        for link in links:
            nodeA = link.find("nodeA") 
            linkName = nodeA.find("name").text
            if nodeA is not None:
                print "link ", linkName, "contains class ", name
            nodeB = link.find("nodeB")
            linkName = nodeB.find("name").text
            if nodeB is not None:
                print "link ", linkName, "contains class ", name

        # debug
        print code

if __name__ == "__main__":
    CppGenerator("apo.xml")
