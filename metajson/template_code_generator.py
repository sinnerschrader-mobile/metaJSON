import os
import datetime
import time

class TemplateCodeGenerator :

    projectPrefix = "S2M"
    TEMPLATE_EXT = ".mustache"
    DEFAULT_TEMPLATE_PATH = "./metajson/templates"

    def __init__(self, template_path = DEFAULT_TEMPLATE_PATH, output_path = "classes"):
        self.template_path = template_path
        self.output_path = output_path
        self.read_template()
        if len(self.json_template_files) == 0:
          print ""

    def read_template(self):
        self.json_template_files = []
        self.general_template_files = []
        for root, dirs, files in os.walk(self.template_path):
            if root == self.template_path:
                for name in files:
                    filepath = os.path.join(root, name)
                    basename, extension = os.path.splitext(filepath)
                    if extension == TemplateCodeGenerator.TEMPLATE_EXT:
                        template_basename, template_extension = os.path.splitext(basename)
                        if template_basename != basename:
                            self.json_template_files.append(filepath)
            else:
                for name in files:
                    filepath = os.path.join(root, name)
                    self.general_template_files.append(filepath)

    def writeNSStringCategory(self) :
        today = datetime.date.fromtimestamp(time.time())

        if not os.path.exists(self.dirPath):
            os.makedirs(self.dirPath)

        headerDstFile = open(self.dirPath + "/NSString+RegExValidation.h", "w")
        headerSrcFile = self.template_path + "/NSString+RegExValidation.h"

        try:
            for line in open(headerSrcFile):
                newLine = line.replace('_DATE_', "")
                newLine = newLine.replace('_YEAR_', str(today.year))
                headerDstFile.write(newLine)
        finally :
            headerDstFile.close()

        implDstFile = open(self.dirPath + "/NSString+RegExValidation.m", "w")
        implSrcFile = self.template_path + "/NSString+RegExValidation.m"

        try:
            for line in open(implSrcFile):
                newLine = line.replace('_DATE_', "")
                newLine = newLine.replace('_YEAR_', str(today.year))
                implDstFile.write(newLine)
        finally :
            implDstFile.close()

    def writeAPIParser(self) :
        today = datetime.date.fromtimestamp(time.time())
        if not os.path.exists(self.dirPath):
            os.makedirs(self.dirPath)

        headerDstFile = open(self.dirPath + "/"+self.projectPrefix+"APIParser.h", "w")
        headerSrcFile = self.template_path + "/APIParser/APIParser.h"


        try:
            for line in open(headerSrcFile):
                newLine = line.replace('_DATE_', "")
                newLine = newLine.replace('_YEAR_', str(today.year))
                newLine = newLine.replace('_PREFIX_', self.projectPrefix)
                headerDstFile.write(newLine)
        finally :
            headerDstFile.close()

        implDstFile = open(self.dirPath + "/"+self.projectPrefix+"APIParser.m", "w")
        implSrcFile = self.template_path + "/APIParser/APIParser.m"

        try:
            for line in open(implSrcFile):
                newLine = line.replace('_DATE_', "")
                newLine = newLine.replace('_YEAR_', str(today.year))
                newLine = newLine.replace('_PREFIX_', self.projectPrefix)
                implDstFile.write(newLine)
        finally :
            implDstFile.close()

    def writeTemplates(self) :

        if self.dirPath.endswith("/") :
            self.dirPath = self.dirPath[:-1]
        baseDirPath = self.dirPath
        self.dirPath = baseDirPath + "/Utilities/NSString"
        self.writeNSStringCategory()
        self.dirPath = baseDirPath + "/Utilities/APIParser"
        self.writeAPIParser()
