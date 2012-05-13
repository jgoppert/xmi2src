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
            self.processClass(classObject)

    def processClass(self,classObject):

        # name
        className = classObject.find("name").text
        if className == None:
            raise IOError("class name not found")
        
        # doc
        doc = classObject.find("doc").text
        if doc == None:
            doc = ""

        parents = classObject.findall("parent")
        for parent in parents:
            print parent.text

        # find all links involving this class
        linkCode=""
        for link in self.root.findall("link"):

            direction = link.find("direction").text

            def processLink(nodeA,nodeB):
                indent="    "
                linkCode=""
                linkClassName = nodeA.find("class").text
                linkType = nodeB.find("class").text
                linkName = nodeA.find("name").text
                if linkClassName == className:
                    linkCode = indent + linkType + " * " + linkName + ";"
                return linkCode

            nodeA = link.find("nodeA")
            nodeB = link.find("nodeB")

            if direction == "a2b":
                linkCode += processLink(nodeA,nodeB)
            elif direction == "b2a":
                linkCode += processLink(nodeB,nodeA)
            elif direction == "both":
                linkCode += processLink(nodeA,nodeB)
                linkCode += processLink(nodeB,nodeA)
            else:
                raise IOError("unknown direction")
            
        # render template
        template = jinja2.Template(open("templates/cpp_class_src.jinja2").read());
        cpp_source = template.render(name=className,doc=doc,links=linkCode)

        # debug
        print cpp_source

        # generate cpp source
        #if not os.path.exists(self.outputPath):
            #os.mkdir(outputPath)
        #f = open("generated_code/"+name+".hpp","w")
        #f.write(cpp_source)
        #f.close()

if __name__ == "__main__":
    CppGenerator("apo.xml")
