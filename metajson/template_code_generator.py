import os
import datetime
import time

class TemplateCodeGenerator :

    projectPrefix = ""
    dirPath = ""
    templatePath = "./metajson/templates"

    def __init__(self):
        projectPrefix = "S2M"
        dirPath = "classes"
        templatePath = "./metajson/templates"

    def writeNSStringCategory(self) :
        today = datetime.date.fromtimestamp(time.time())

        if not os.path.exists(self.dirPath):
            os.makedirs(self.dirPath)

        headerDstFile = open(self.dirPath + "/NSString+RegExValidation.h", "w")
        headerSrcFile = self.templatePath + "/NSString+RegExValidation.h"

        try:
            for line in open(headerSrcFile):
                newLine = line.replace('_DATE_', "")
                newLine = newLine.replace('_YEAR_', str(today.year))
                headerDstFile.write(newLine)
        finally :
            headerDstFile.close()

        implDstFile = open(self.dirPath + "/NSString+RegExValidation.m", "w")
        implSrcFile = self.templatePath + "/NSString+RegExValidation.m"

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
        headerSrcFile = self.templatePath + "/APIParser/APIParser.h"


        try:
            for line in open(headerSrcFile):
                newLine = line.replace('_DATE_', "")
                newLine = newLine.replace('_YEAR_', str(today.year))
                newLine = newLine.replace('_PREFIX_', self.projectPrefix)
                headerDstFile.write(newLine)
        finally :
            headerDstFile.close()

        implDstFile = open(self.dirPath + "/"+self.projectPrefix+"APIParser.m", "w")
        implSrcFile = self.templatePath + "/APIParser/APIParser.m"

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
