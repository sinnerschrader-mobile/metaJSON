'''
The MIT License (MIT)

Copyright (c) 2013 SinnerSchrader Mobile GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import datetime
import time
import os
import sys
from pystache import Renderer
# import pickle
# from cStringIO import StringIO


class ObjectiveCCodeGenerator :

    projectPrefix = ""
    dirPath = ""

    def __init__(self):
        projectPrefix = ""
        dirPath = "classes"

    def template_file_path(self, filename) :
        templatePath = os.path.realpath( __file__ )
        templatePath = templatePath.replace(os.path.basename( __file__ ), 'templates')
        return os.path.join(templatePath, filename)

    def makeVarName(self,schemeObj) :
        returnName = schemeObj.type_name
        if str(schemeObj.type_name) == "id" or str(schemeObj.type_name) == "description" :
            titleName = schemeObj.type_name.upper()
            titleName = titleName[:1] + schemeObj.type_name[1:]
            returnName = self.projectPrefix.lower() + titleName
        else :
            prefixes = ["new", "alloc", "copy"]
            for prefix in prefixes:
                if schemeObj.type_name.startswith(prefix):
                    titleName = schemeObj.type_name.upper()
                    titleName = titleName[:1] + schemeObj.type_name[1:]
                    returnName = self.projectPrefix.lower() + titleName
                    #print returnName
                    break

        return returnName

    def process_properties(self, propObj) :
        propertyHash = {"declaration": self.propertyDefinitionString(propObj)}
        if propObj.type_description and len(propObj.type_description) :
            propertyHash["comment"] = propObj.type_description
        return propertyHash

    def human_header_content(self, schemeObj) :
        templateFile = open(self.template_file_path("header.h.mustache"), "r")
        today = datetime.date.fromtimestamp(time.time())

        hashParams = {"date": str(today.year), "machineClassName": schemeObj.getMachineClassName(), "humanClassName": schemeObj.getClassName()}
        return Renderer().render(templateFile.read(), hashParams)

    def human_source_content(self, schemeObj) :
        templateFile = open(self.template_file_path("source.m.mustache"), "r")
        today = datetime.date.fromtimestamp(time.time())

        hashParams = {"date": str(today.year), "machineClassName": schemeObj.getMachineClassName(), "humanClassName": schemeObj.getClassName()}
        return Renderer().render(templateFile.read(), hashParams)

    def machine_header_content(self, schemeObj) :
        templateFile = open(self.template_file_path("_header.h.mustache"), "r")
        today = datetime.date.fromtimestamp(time.time())
        props = []
        for prop in schemeObj.props:
            props.append(self.process_properties(prop))
        hashParams = {"date": str(today.year), "machineClassName": schemeObj.getMachineClassName(), "humanClassName": schemeObj.getClassName(), "variableName": self.makeVarName(schemeObj), "properties": props}
        # print "hashParams"
        # print hashParams

        return Renderer().render(templateFile.read(), hashParams)

    def machine_source_content(self, schemeObj) :
        templateFile = open(self.template_file_path("_source.m.mustache"), "r")
        today = datetime.date.fromtimestamp(time.time())

        props = []
        for prop in schemeObj.props:
            props.append(prop.__dict__)
        print props

        # retrieve all params for template
        hashParams = {"date": str(today.year), "machineClassName": schemeObj.getMachineClassName(), "projectPrefix": self.projectPrefix, "humanClassName": schemeObj.getClassName(), "variableName": self.makeVarName(schemeObj), "properties": props}

        # render
        sourceString = Renderer().render(templateFile.read(), hashParams)


        return sourceString

    def make(self, schemeObj) :
        # machine files
        self.write_abstract_file(schemeObj.getMachineClassName() + ".h", self.machine_header_content(schemeObj))
        self.write_abstract_file(schemeObj.getMachineClassName() + ".m", self.machine_source_content(schemeObj))

        # human files
        self.write_human_file(schemeObj.getClassName() + ".h", self.human_header_content(schemeObj))
        self.write_human_file(schemeObj.getClassName() + ".m",  self.human_source_content(schemeObj))

        return True

    def write_abstract_file(self, filename, content) :
        folder = "/AbstractInterfaceFiles/"
        if not os.path.exists(self.dirPath + folder):
            os.makedirs(self.dirPath + folder)

        filepath = self.dirPath + folder + filename
        self.write_file(filepath, content)

    def write_human_file(self, filename, content) :
        folder = "/"
        if not os.path.exists(self.dirPath + folder):
            os.makedirs(self.dirPath + folder)

        filepath = self.dirPath + folder + filename
        self.write_file(filepath, content)

    def write_file(self, filename, content) :
        if not os.path.exists(self.dirPath):
            os.makedirs(self.dirPath)

        if self.dirPath.endswith("/") :
            self.dirPath = self.dirPath[:-1]


        if os.path.isfile(filename) is False :
            print "create " + filename + " file..."
            try:
                writefile = open(filename, "w")
                writefile.write(content) # Write a string to a file
            finally :
                writefile.close()


    """
    getter method
    """
    def getterMethodDefinitionStringInDictionary(self, returnTypeName, typeName, typeTitle, postFix) :
        return "- (" + returnTypeName + ")" + typeName + "As" + typeTitle + postFix

    def getterMethodDefinitionStringInArray(self, returnTypeName, typeName, arrayName, postFix) :
        return "- (" + returnTypeName + ")" + typeName + "In"+  arrayName + postFix

    def getTitledString(self, inputString) :
        titledString = inputString.upper()
        titledString = titledString[:1] + inputString[1:]
        return titledString

    def getNaturalTypeClassTitleString(self,typeName) :
        titleString = self.getTitledString(typeName)
        if typeName == "boolean" or typeName == "string" or typeName == "date" or typeName == "data" or typeName == "number" or typeName == "array" :
            return titleString
        else :
            return "Object"

    def getNaturalTypeClassString(self,typeName) :
        if typeName == "boolean" :
            return "BOOL "
        elif typeName == "string" :
            return "NSString *"
        elif typeName == "date" :
            return "NSDate *"
        elif typeName == "data" :
            return "NSData *"
        elif typeName == "number" :
            return "NSNumber *"
        elif typeName == "array" :
            return "NSArray *"
        else :
            return "id "

    def getterMethodDefinitionString(self, schemeObj) :
        resultStringList= []

        titleName = schemeObj.type_name.upper()
        titleName = titleName[:1] + schemeObj.type_name[1:]
        postFix = ":(NSError **)error;\n"

        if schemeObj.rootBaseType() == "multi" :
            for schemeName in schemeObj.getBaseTypes() :
                #print "(getterMethodDefinitionString : multi) : find scheme : " + schemeName + " from : " + schemeObj.type_name
                if schemeObj.hasScheme(schemeName) :
                    baseSubTypeSchemeObj = schemeObj.getScheme(schemeName)
                    baseSubTypeTitle = baseSubTypeSchemeObj.type_name.upper()
                    baseSubTypeTitle = baseSubTypeTitle[:1] + baseSubTypeSchemeObj.type_name[1:]

                    if baseSubTypeSchemeObj.isNaturalType() == False :
                        resultStringList.append(self.getterMethodDefinitionStringInDictionary(baseSubTypeSchemeObj.getClassName() + " *", schemeObj.type_name, baseSubTypeSchemeObj.getClassName(), postFix))
                    else :
                        resultStringList.append(self.getterMethodDefinitionStringInDictionary(self.getNaturalTypeClassString(baseSubTypeSchemeObj.rootBaseType()), schemeObj.type_name, baseSubTypeTitle, postFix))

                elif schemeName == "any" :
                    resultStringList.append(self.getterMethodDefinitionStringInDictionary("id", schemeObj.type_name, "Object", postFix))
                else :
                    resultStringList.append(self.getterMethodDefinitionStringInDictionary(self.getNaturalTypeClassString(schemeName), schemeObj.type_name, self.getNaturalTypeClassTitleString(schemeName),postFix))

        elif schemeObj.rootBaseType() == "array" :
            postFix = "AtIndex:(NSUInteger)index withError:(NSError **)error;\n";
            for schemeName in schemeObj.getSubType() :
                #print "(getterMethodDefinitionString : array) : find scheme : " + schemeName + " from : " + schemeObj.type_name
                if schemeObj.hasScheme(schemeName) :
                    baseSubTypeSchemeObj = schemeObj.getScheme(schemeName)

                    if baseSubTypeSchemeObj.isNaturalType() == False :
                        resultStringList.append(self.getterMethodDefinitionStringInArray(baseSubTypeSchemeObj.getClassName() + " *", baseSubTypeSchemeObj.type_name, titleName, postFix))
                    else :
                        resultStringList.append(self.getterMethodDefinitionStringInArray(self.getNaturalTypeClassString(baseSubTypeSchemeObj.rootBaseType()), baseSubTypeSchemeObj.type_name, titleName, postFix))

                elif schemeName == "any" :
                    resultStringList.append(self.getterMethodDefinitionStringInArray("id", "object", titleName, postFix))
                else :
                    resultStringList.append(self.getterMethodDefinitionStringInArray(self.getNaturalTypeClassString(schemeName), schemeName, titleName, postFix))

        elif schemeObj.base_type == "any"  :
            resultStringList.append(self.getterMethodDefinitionStringInDictionary("id", schemeObj.type_name, "Object", postFix))

        elif schemeObj.isNaturalType() :
            print "Error : " + schemeObj.type_name + " is Natural type. don't need to define getter method.\n"
            resultStringList = []

        else :
            print "Error : " + schemeObj.type_name + " is Custom Object type. don't need to define getter method.\n"
            resultStringList = []

        return resultStringList

    def getterMethodString(self, schemeObj) :
        resultString = ""
        postFix = ":(NSError **)error {\n"
        titleName = schemeObj.type_name.upper()
        titleName = titleName[:1] + schemeObj.type_name[1:]
        tmpVarName = "tmp" + self.getTitledString(schemeObj.type_name)
        selfDicName = "self." + self.makeVarName(schemeObj)

        if schemeObj.rootBaseType() == "multi" :
            for schemeName in schemeObj.getBaseTypes() :
                #print "(getterMethodString : multi) : find scheme : " + schemeName + " from : " + schemeObj.type_name
                if schemeObj.hasScheme(schemeName) :
                    baseSubTypeSchemeObj = schemeObj.getScheme(schemeName)
                    baseSubTypeTitle = baseSubTypeSchemeObj.type_name.upper()
                    baseSubTypeTitle = baseSubTypeTitle[:1] + baseSubTypeSchemeObj.type_name[1:]

                    if baseSubTypeSchemeObj.isNaturalType() == False :
                        tmpDicName = "tmp" + self.getTitledString(schemeObj.type_name) + "Dic"
                        resultString += self.getterMethodDefinitionStringInDictionary(baseSubTypeSchemeObj.getClassName() + " *", schemeObj.type_name, baseSubTypeSchemeObj.getClassName(), postFix)
                        resultString += self.getDictionaryGetterFromDictionaryCode(tmpDicName, selfDicName, schemeObj.type_name, (schemeObj.required != True), 1, "nil")
                        resultString += self.getHandleErrorCode( tmpDicName +" == nil", "", "nil", 1)
                        resultString += "    " + baseSubTypeSchemeObj.getClassName() + " *" + tmpVarName + " = nil;\n"
                        resultString += self.getObjectAllocatorFromDictionaryCode(False, baseSubTypeSchemeObj.getClassName(), tmpVarName, tmpDicName, (schemeObj.required != True), 1, "nil")
                        resultString += "    return " + tmpVarName + ";\n}\n"
                    else :
                        resultString += self.getterMethodDefinitionStringInDictionary(self.getNaturalTypeClassString(baseSubTypeSchemeObj.rootBaseType()), schemeObj.type_name, baseSubTypeTitle, postFix)
                        resultString += self.getNaturalTypeGetterFromDictionaryCode(baseSubTypeSchemeObj, self.getNaturalTypeClassString(baseSubTypeSchemeObj.rootBaseType()), tmpVarName, selfDicName, schemeObj.type_name, (schemeObj.required != True), 1, "nil")
                        resultString += self.getHandleErrorCode( tmpVarName +" == nil", "", "nil", 1)
                        resultString += self.getNaturalTypeValidationCode(baseSubTypeSchemeObj, tmpVarName, 1, "nil")
                        resultString += "    return " + tmpVarName + ";\n}\n"

                elif schemeName == "any" :
                    resultString += self.getterMethodDefinitionStringInDictionary("id", schemeObj.type_name, "Object", postFix)
                    resultString += self.getUndefinedTypeGetterFromDictionaryCode("id ", tmpVarName, selfDicName, schemeObj.type_name, (schemeObj.required != True), 1, "nil")
                    resultString += "    return " + tmpVarName + ";\n}\n"
                else :
                    resultString += self.getterMethodDefinitionStringInDictionary(self.getNaturalTypeClassString(schemeName), schemeObj.type_name, self.getNaturalTypeClassTitleString(schemeName),postFix)
                    resultString += self.getNaturalTypeGetterFromDictionaryCode(schemeName, self.getNaturalTypeClassString(schemeName), tmpVarName, selfDicName, schemeObj.type_name, (schemeObj.required != True), 1, "nil")
                    resultString += "    return " + tmpVarName + ";\n}\n"

        elif schemeObj.rootBaseType() == "array" :
            postFix = "AtIndex:(NSUInteger)index withError:(NSError **)error {\n";
            for schemeName in schemeObj.getSubType() :
                if schemeObj.hasScheme(schemeName) :
                    #print "(getterMethodString : array) : find scheme : " + schemeName + " from : " + schemeObj.type_name
                    baseSubTypeSchemeObj = schemeObj.getScheme(schemeName)

                    if baseSubTypeSchemeObj.isNaturalType() == False :
                        tmpDicName = "tmp" + self.getTitledString(schemeObj.type_name) + "Dic"
                        resultString += self.getterMethodDefinitionStringInArray(baseSubTypeSchemeObj.getClassName() + " *", baseSubTypeSchemeObj.type_name, titleName, postFix)
                        resultString += self.getDictionaryGetterFromArrayCode(tmpDicName, selfDicName, "index", (schemeObj.required != True), 1, "nil")
                        resultString += "    " + baseSubTypeSchemeObj.getClassName() + " *" + tmpVarName + " = nil;\n"
                        resultString += self.getHandleErrorCode( tmpDicName +" == nil", "", "nil", 1)
                        resultString += self.getObjectAllocatorFromDictionaryCode(False, baseSubTypeSchemeObj.getClassName(), tmpVarName, tmpDicName, (schemeObj.required != True), 1, "nil")
                        resultString += "    return " + tmpVarName + ";\n}\n"

                    else :
                        resultString += self.getterMethodDefinitionStringInArray(self.getNaturalTypeClassString(baseSubTypeSchemeObj.rootBaseType()), baseSubTypeSchemeObj.type_name,titleName,postFix)
                        resultString += self.getNaturalTypeGetterFromArrayCode(baseSubTypeSchemeObj, self.getNaturalTypeClassString(baseSubTypeSchemeObj.rootBaseType()), tmpVarName, selfDicName, "index", (schemeObj.required != True), 1, "nil")
                        resultString += self.getNaturalTypeValidationCode(baseSubTypeSchemeObj, tmpVarName, 1, "nil")
                        resultString += "    return " + tmpVarName + ";\n}\n"


                elif schemeName == "any" :
                    resultString += self.getterMethodDefinitionStringInArray("id", "object", titleName, postFix)
                    resultString += self.getGetterFromArrayCode("id ", tmpVarName, selfDicName, "index", (schemeObj.required != True), 1, "nil")
                    resultString += "    return " + tmpVarName + ";\n}\n"
                else :
                    resultString += self.getterMethodDefinitionStringInArray(self.getNaturalTypeClassString(schemeName), schemeName, titleName, postFix)
                    resultString += self.getNaturalTypeGetterFromArrayCode(schemeName, self.getNaturalTypeClassString(schemeName), tmpVarName, selfDicName, "index", (schemeObj.required != True), 1, "nil")
                    resultString += "    return " + tmpVarName + ";\n}\n"

        elif schemeObj.base_type == "any"  :
            resultString += self.getterMethodDefinitionStringInDictionary("id", schemeObj.type_name, "Object", postFix)
            resultString += self.getUndefinedTypeGetterFromDictionaryCode("id ", tmpVarName, selfDicName, schemeObj.type_name, (schemeObj.required != True), 1, "nil")
            resultString += "    return " + tmpVarName + ";\n}\n"

        elif schemeObj.isNaturalType() :
            print "Error : " + schemeObj.type_name + " is Natural type. don't need to implement getter method.\n"
            return "#error " + schemeObj.type_name + " is Natural type. don't need to implement getter method.\n"

        else :
            print "Error : " + schemeObj.type_name + " is Custom Object type. don't need to implement getter method.\n"
            return "#error " + schemeObj.type_name + " is Custom Object type. don't need to implement getter method.\n"

        return resultString

    def getIndentString(self, indentDepth) :
        resultString = ""
        indentString = "    "
        for loop in range(indentDepth) :
            resultString += indentString

        return resultString

    def getHandleErrorCode(self, statement, errorString, returnVarName, indentDepth) :
        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)
        resultString += firstIndent + "if ("+ statement + ") {\n"
        if len(errorString) :
            resultString += secondIndent + errorString
        resultString += secondIndent + "return " + returnVarName + ";\n" + firstIndent + "}\n"
        return  resultString

    def getStringValidationCode(self, schemeObj, varName, indentDepth, returnVarName) :
        resultString = ""
        statementString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)
        errorString = "NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@\"" + self.makeVarName(schemeObj) + "\", @\"propertyName\", @\"" + schemeObj.type_name + "\", @\"key\", @\"validation error\", @\"reason\", NSStringFromClass([self class]), @\"objectClass\",nil];\n"
        errorString += secondIndent + "*error = [NSError errorWithDomain:k" + self.projectPrefix + "ErrorDomain_parser code:k" + self.projectPrefix + "ErrorDomain_parser_valueIsNotValid userInfo:userInfo];\n"
        errorString += secondIndent + "NSLog(@\"%@\", *error);\n"

        maxResult = schemeObj.getMaxLength()

        if maxResult[0] :
            statementString = str(varName) + ".length > " + str(maxResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        minResult = schemeObj.getMinLength()
        if minResult[0] :
            statementString = varName + ".length < " + str(minResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        regExResult = schemeObj.getRegex()
        if regExResult[0] :
            statementString = varName + " && ["+varName+" matchesRegExString:@\"" +str(regExResult[1])+ "\"] == NO"
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        return resultString

    def getDateValidationCode(self, schemeObj, varName, indentDepth, returnVarName) :
        resultString = ""
        statementString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)
        errorString = "NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@\"" + self.makeVarName(schemeObj) + "\", @\"propertyName\", @\"" + schemeObj.type_name + "\", @\"key\", @\"validation error\", @\"reason\", NSStringFromClass([self class]), @\"objectClass\",nil];\n"
        errorString += secondIndent + "*error = [NSError errorWithDomain:k" + self.projectPrefix + "ErrorDomain_parser code:k" + self.projectPrefix + "ErrorDomain_parser_valueIsNotValid userInfo:userInfo];\n"
        errorString += secondIndent + "NSLog(@\"%@\", *error);\n"

        maxResult = schemeObj.getMaxValue()
        if maxResult[0] :
            statementString = "["+varName+" timeIntervalSince1970] > " + str(maxResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        minResult = schemeObj.getMinValue()
        if minResult[0] :
            statementString = "["+varName+" timeIntervalSince1970] < " + str(minResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        return resultString

    def getDataValidationCode(self, schemeObj, varName, indentDepth, returnVarName) :
        resultString = ""
        statementString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)
        errorString = "NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@\"" + self.makeVarName(schemeObj) + "\", @\"propertyName\", @\"" + schemeObj.type_name + "\", @\"key\", @\"validation error\", @\"reason\", NSStringFromClass([self class]), @\"objectClass\",nil];\n"
        errorString += secondIndent + "*error = [NSError errorWithDomain:k" + self.projectPrefix + "ErrorDomain_parser code:k" + self.projectPrefix + "ErrorDomain_parser_valueIsNotValid userInfo:userInfo];\n"
        errorString += secondIndent + "NSLog(@\"%@\", *error);\n"

        maxResult = schemeObj.getMaxLength()
        if maxResult[0] :
            statementString = varName+".length > " + str(maxResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        minResult = schemeObj.getMinLength()
        if minResult[0] :
            statementString = varName+".length < " + str(minResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        return resultString

    def getNumberValidationCode(self, schemeObj, varName, indentDepth, returnVarName) :
        resultString = ""
        statementString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)
        errorString = "NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@\"" + self.makeVarName(schemeObj) + "\", @\"propertyName\", @\"" + schemeObj.type_name + "\", @\"key\", @\"validation error\", @\"reason\", NSStringFromClass([self class]), @\"objectClass\",nil];\n"
        errorString += secondIndent + "*error = [NSError errorWithDomain:k" + self.projectPrefix + "ErrorDomain_parser code:k" + self.projectPrefix + "ErrorDomain_parser_valueIsNotValid userInfo:userInfo];\n"
        errorString += secondIndent + "NSLog(@\"%@\", *error);\n"

        maxResult = schemeObj.getMaxValue()
        if maxResult[0] :
            statementString = "["+varName+" floatValue] > " + str(maxResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        minResult = schemeObj.getMinValue()
        if minResult[0] :
            statementString = "["+varName+" floatValue] < " + str(minResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)
        return resultString

    def getArrayValidationCode(self, schemeObj, varName, indentDepth, returnVarName) :
        resultString = ""
        statementString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)
        errorString = "NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@\"" + self.makeVarName(schemeObj) + "\", @\"propertyName\", @\"" + schemeObj.type_name + "\", @\"key\", @\"validation error\", @\"reason\", NSStringFromClass([self class]), @\"objectClass\",nil];\n"
        errorString += secondIndent + "*error = [NSError errorWithDomain:k" + self.projectPrefix + "ErrorDomain_parser code:k" + self.projectPrefix + "ErrorDomain_parser_valueIsNotValid userInfo:userInfo];\n"
        errorString += secondIndent + "NSLog(@\"%@\", *error);\n"

        maxResult = schemeObj.getMaxCount()
        if maxResult[0] :
            statementString = varName+".count > " + str(maxResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        minResult = schemeObj.getMinCount()
        if minResult[0] :
            statementString = varName+".count < " + str(minResult[1])
            resultString += self.getHandleErrorCode(statementString, errorString, returnVarName, indentDepth)

        return resultString

    def getNaturalTypeValidationCode(self, schemeObj, varName, indentDepth, returnVarName) :
        if schemeObj.isNaturalType() :
            if schemeObj.rootBaseType() == "array" :
                return self.getArrayValidationCode(schemeObj, varName, indentDepth, returnVarName)
            elif schemeObj.rootBaseType() == "string" :
                return self.getStringValidationCode(schemeObj, varName, indentDepth, returnVarName)
            elif schemeObj.rootBaseType() == "number" :
                return self.getNumberValidationCode(schemeObj, varName, indentDepth, returnVarName)
            elif schemeObj.rootBaseType() == "date" :
                return self.getDateValidationCode(schemeObj, varName, indentDepth, returnVarName)
            elif schemeObj.rootBaseType() == "data" :
                return self.getDataValidationCode(schemeObj, varName, indentDepth, returnVarName)

        return ""


    def getNaturalTypeGetterFromDictionaryCode(self, schemeObj, className, varName, dicName, keyName, allowNull, indentDepth, returnVarName) :
        schemeBaseType = ""
        if type(schemeObj) == str or type(schemeObj) == unicode:
            schemeBaseType = str(schemeObj)
        elif schemeObj.isNaturalType() :
            schemeBaseType = str(schemeObj.rootBaseType())
        else :
            print "Error (getNaturalTypeGetterFromDictionaryCode): undfined scheme base type " + schemeObj
            return "#error - undfined scheme base type\n"
        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)

        if schemeBaseType == "array" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser arrayFromResponseDictionary:" + dicName + " forKey:@\"" + keyName + "\" acceptNil:"
        elif schemeBaseType == "string" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser stringFromResponseDictionary:" + dicName + " forKey:@\"" + keyName + "\" acceptNumber:NO acceptNil:"
        elif schemeBaseType == "number" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser numberFromResponseDictionary:" + dicName + " forKey:@\"" + keyName + "\" acceptNil:"
        elif schemeBaseType == "date" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser dateWithTimeIntervalFromResponseDictionary:" + dicName + " forKey:@\"" + keyName + "\" acceptNil:"
        elif schemeBaseType == "data" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser dataFromResponseDictionary:" + dicName + " forKey:@\"" + keyName + "\" acceptNil:"
        elif schemeBaseType == "boolean" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser boolFromResponseDictionary:" + dicName + " forKey:@\"" + keyName + "\" acceptNil:"
        else :
            print "Error (getNaturalTypeGetterFromDictionaryCode): undfined scheme natural base type " + schemeObj
            return "#error - undfined scheme natural base type\n"

        if allowNull :
            resultString += "YES"
        else :
            resultString += "NO"
        resultString += " error:error];\n"
        resultString += self.getHandleErrorCode("*error", "", returnVarName, indentDepth)

        return resultString

    def getUndefinedTypeGetterFromDictionaryCode(self, className, varName, dicName, keyName, allowNull, indentDepth, returnVarName) :
        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)

        resultString += firstIndent
        if className and len(className) :
            resultString += className
        resultString += varName + " = [" + self.projectPrefix + "APIParser objectFromResponseDictionary:" + dicName + " forKey:@\"" + keyName + "\" acceptNil:"

        if allowNull :
            resultString += "YES"
        else :
            resultString += "NO"
        resultString += " error:error];\n"
        resultString += self.getHandleErrorCode("*error", "", returnVarName, indentDepth)

        return resultString

    def getNaturalTypeGetterFromArrayCode(self, schemeObj, className, varName, arrayName, indexVar, allowNull, indentDepth, returnVarName) :
        schemeBaseType = ""
        if type(schemeObj) == str or type(schemeObj) == unicode:
            schemeBaseType = str(schemeObj)
        elif schemeObj.isNaturalType() :
            schemeBaseType = str(schemeObj.rootBaseType())
        else :
            print "Error (getNaturalTypeGetterFromArrayCode): undfined scheme base type " + schemeObj
            return "#error - undfined scheme base type\n"

        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)

        if schemeBaseType == "array" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser arrayFromResponseArray:" + arrayName + " atIndex:" + indexVar + " acceptNil:"
        elif schemeBaseType == "string" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser stringFromResponseArray:" + arrayName + " atIndex:" + indexVar + " acceptNil:"
        elif schemeBaseType == "number" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser numberFromResponseArray:" + arrayName + " atIndex:" + indexVar + " acceptNil:"
        elif schemeBaseType == "date" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser dateWithTimeIntervalFromResponseArray:" + arrayName + " atIndex:" + indexVar + " acceptNil:"
        elif schemeBaseType == "data" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser dataFromResponseArray:" + arrayName + " atIndex:" + indexVar + " acceptNil:"
        elif schemeBaseType == "boolean" :
            resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser boolFromResponseArray:" + arrayName + " atIndex:" + indexVar + " acceptNil:"
        else :
            print "Error (getNaturalTypeGetterFromArrayCode): undfined scheme natural base type " + schemeObj
            return "#error - undfined scheme natural base type\n"

        if allowNull :
            resultString += "YES"
        else :
            resultString += "NO"
        resultString += " error:error];\n"
        resultString += self.getHandleErrorCode("*error", "", returnVarName, indentDepth)

        return resultString

    def getDictionaryGetterFromDictionaryCode(self, varName, dicName, keyName, allowNull, indentDepth, returnVarName) :
        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)

        resultString += firstIndent + "NSDictionary *"+ varName + " = [" + self.projectPrefix + "APIParser dictionaryFromResponseDictionary:" + dicName + " forKey:@\"" + keyName + "\" acceptNil:"
        if allowNull :
            resultString += "YES"
        else :
            resultString += "NO"
        resultString += " error:error];\n"
        resultString += self.getHandleErrorCode("*error", "", returnVarName, indentDepth)
        return resultString

    def getDictionaryGetterFromArrayCode(self, varName, arrayName, indexVar, allowNull, indentDepth, returnVarName) :
        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)

        resultString += firstIndent + "NSDictionary *"+ varName + " = [" + self.projectPrefix + "APIParser dictionaryFromResponseArray:" + arrayName + " atIndex:" + indexVar + " acceptNil:"
        if allowNull :
            resultString += "YES"
        else :
            resultString += "NO"
        resultString += " error:error];\n"
        resultString += self.getHandleErrorCode("*error", "", returnVarName, indentDepth)

        return resultString

    def getObjectAllocatorFromDictionaryCode(self, defineClass, className, varName, dicName, allowNull, indentDepth, returnVarName) :
        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)
        resultString += firstIndent + "if (" + dicName + ") {\n"
        resultString += secondIndent
        if defineClass :
            resultString += className+ " *"
        resultString += varName + "= [[" + className + " alloc] initWithDictionary:" + dicName + " withError:error];\n"
        resultString += self.getHandleErrorCode("*error", "", returnVarName, indentDepth + 1)
        resultString += firstIndent + "}\n"

        return resultString

    def getDictionaryAllocatorCode(self, defineClass, varName, objectName, keyNmae, indentDepth, returnVarName) :
        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)

        resultString += firstIndent
        if defineClass :
            resultString += "NSDictionary *"
        resultString += varName + " = [NSDictionary dictionaryWithObjectsAndKeys:"+ objectName +", @\"" + keyNmae + "\", nil];\n"

        return resultString

    def getGetterFromDictionaryCode(self, className, varName, dicName, keyName, allowNull, indentDepth, returnVarName) :
        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)

        resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser objectFromResponseDictionary:" + dicName + " forKey:@\"" + keyName + "\" acceptNil:"
        if allowNull :
            resultString += "YES"
        else :
            resultString += "NO"

        resultString += " error:error];\n"
        resultString += self.getHandleErrorCode("*error", "", returnVarName, indentDepth)
        return resultString

    def getGetterFromArrayCode(self, className, varName, arrayName, indexVar, allowNull, indentDepth, returnVarName) :
        resultString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth+1)
        resultString += firstIndent + className + varName + " = [" + self.projectPrefix + "APIParser objectFromResponseArray:" + arrayName + " atIndex:" + indexVar
        resultString += " acceptNil:"
        if allowNull :
            resultString += "YES"
        else :
            resultString += "NO"
        resultString += " error:error];\n"
        resultString += self.getHandleErrorCode("*error", "", returnVarName, indentDepth)
        return resultString

    def propertyDefinitionString(self, schemeObj) :
        resultString = ""

        if schemeObj.isNaturalType() :
            if schemeObj.rootBaseType() == "boolean" :
                return "@property (nonatomic, assign) BOOL " + self.makeVarName(schemeObj) + ";"
            elif schemeObj.rootBaseType() == "string" :
                return "@property (nonatomic, strong) NSString *" + self.makeVarName(schemeObj) + ";"
            elif schemeObj.rootBaseType() == "date" :
                return "@property (nonatomic, strong) NSDate *" + self.makeVarName(schemeObj) + ";"
            elif schemeObj.rootBaseType() == "data" :
                return "@property (nonatomic, strong) NSData *" + self.makeVarName(schemeObj) + ";"
            elif schemeObj.rootBaseType() == "number" :
                return "@property (nonatomic, strong) NSNumber *" + self.makeVarName(schemeObj) + ";"
            elif schemeObj.rootBaseType() == "array" :
                return "@property (nonatomic, strong) NSArray *" + self.makeVarName(schemeObj) + ";"
            else :
                return "@property (nonatomic, strong) id " + self.makeVarName(schemeObj) + ";"

        elif schemeObj.rootBaseType() == "multi" or schemeObj.rootBaseType() == "any" :
            return "@property (nonatomic, strong) NSDictionary *" + self.makeVarName(schemeObj) + ";"


        return "@property (nonatomic, strong) "+ schemeObj.getClassName() +" *" + self.makeVarName(schemeObj) + ";"

    def propertyDecodeString(self, schemeObj, indentDepth) :
        firstIndent = self.getIndentString(indentDepth)
        if schemeObj.isNaturalType() and schemeObj.rootBaseType() == "boolean" :
            return firstIndent +  "self." + self.makeVarName(schemeObj) + " = [coder decodeBoolForKey:@\"" + schemeObj.type_name + "\"];\n"

        return firstIndent + "self." + self.makeVarName(schemeObj) + " = [coder decodeObjectForKey:@\"" + schemeObj.type_name + "\"];\n"

    def propertyEncodeString(self, schemeObj, indentDepth) :
        firstIndent = self.getIndentString(indentDepth)
        if schemeObj.isNaturalType() and schemeObj.rootBaseType() == "boolean" :
            return firstIndent + "[coder encodeBool:self." + self.makeVarName(schemeObj)+ " forKey:@\"" + schemeObj.type_name+"\"];\n"

        return firstIndent + "[coder encodeObject:self." + self.makeVarName(schemeObj)+ " forKey:@\"" + schemeObj.type_name+"\"];\n"

    def setPropertyDictionaryString(self, schemeObj, dicName, indentDepth) :
        returnString = ""
        firstIndent = self.getIndentString(indentDepth)
        secondIndent = self.getIndentString(indentDepth + 1)
        thirdIndent = self.getIndentString(indentDepth + 2)
        returnString += firstIndent + "if (self." + self.makeVarName(schemeObj) + ") {\n"
        if schemeObj.isNaturalType() :
            if schemeObj.rootBaseType() == "boolean" :
                returnString += secondIndent + "[" + dicName+ " setObject:[NSNumber numberWithBool:self." + self.makeVarName(schemeObj) + "] forKey:@\"" + schemeObj.type_name + "\"];\n"
            elif schemeObj.rootBaseType() == "date" :
                returnString += secondIndent + "[" + dicName+ " setObject:[NSNumber numberWithInteger:[[NSNumber numberWithDouble:[self." + self.makeVarName(schemeObj) + " timeIntervalSince1970]] longValue]] forKey:@\"" + schemeObj.type_name + "\"];\n";
            elif schemeObj.rootBaseType() == "array" :
                arrayObjType = schemeObj.getSubType()
                if arrayObjType and len(arrayObjType) == 1 and schemeObj.hasScheme(arrayObjType[0]) == True :
                    arraySchemeObj = schemeObj.getScheme(arrayObjType[0])
                    returnString += secondIndent + "NSMutableArray *tmpArray = [[NSMutableArray alloc] init];\n"
                    if arraySchemeObj.rootBaseType() == "object" :
                        returnString += secondIndent + "for (" + arraySchemeObj.getClassName() + " *tmpObj in self." + self.makeVarName(schemeObj) + ") {\n"
                        returnString += thirdIndent + "[tmpArray addObject:[tmpObj propertyDictionary]];\n"
                    else :
                        returnString += secondIndent + "for (id tmpObj in self." + self.makeVarName(schemeObj) + ") {\n"
                        returnString += thirdIndent + "[tmpArray addObject:tmpObj];\n"

                    returnString += secondIndent + "}\n"
                    returnString += secondIndent + "[" + dicName + " setObject:tmpArray forKey:@\"" + schemeObj.type_name + "\"];\n"
                else :
                    returnString += secondIndent + "[" + dicName + " setObject:self." + self.makeVarName(schemeObj) + " forKey:@\"" + schemeObj.type_name + "\"];\n"
            else :
                returnString += secondIndent + "[" + dicName + " setObject:self." + self.makeVarName(schemeObj) + " forKey:@\"" + schemeObj.type_name + "\"];\n"
        elif schemeObj.rootBaseType() == "multi" or schemeObj.rootBaseType() == "any" :
                returnString += secondIndent + "[" + dicName + " setObject:self." + self.makeVarName(schemeObj) + " forKey:@\"" + schemeObj.type_name + "\"];\n"
        else :
            returnString += secondIndent + "[" + dicName + " setObject:[self." + self.makeVarName(schemeObj) + " propertyDictionary] forKey:@\"" + schemeObj.type_name + "\"];\n"

        returnString += firstIndent + "}\n"
        return returnString


class TemplateCodeGenerator :

    projectPrefix = ""
    dirPath = ""
    templatePath = "./templates"

    def __init__(self):
        projectPrefix = "S2M"
        dirPath = "classes"
        templatePath = "./templates"
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
