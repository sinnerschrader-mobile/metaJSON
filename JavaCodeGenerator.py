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

import time
import datetime
import os

class JavaCodeGenerator:
    naturalList = ["Object", "String", "double", "boolean", "Double", "Boolean"]
    projectPrefix = ""
    dirPath = ""
    memberVariables = ""
    isChild = False
    isAbstract = False

    def getCommonDescriptionString(self):
        today = datetime.date.fromtimestamp(time.time())
        commonDescription = "/*\n *  Created by MetaJSONParser on " + today.strftime("%d.%m.%Y") + "."
        commonDescription += "\n *  Copyright (c) " + str(today.year) + " SinnerSchrader Mobile. All rights reserved.\n*/\n"
        return commonDescription

    def make(self, schemeObj):
        self.makeInternal(schemeObj)
        self.makeExtension(schemeObj)
        return True

    def makeInternal(self, schemeObj):
        self.isAbstract = True
        sourceString = ""
        self.isChild = False;
        print "starting: " + self.getClassName(schemeObj)

        if len(self.dirPath) > 0:
            sourceString += "package " + self.dirPath.replace("/", ".") + ".internal;\n\n"
        sourceString += self.getCommonDescriptionString()
        sourceString += self.getImports(schemeObj)
        sourceString += self.getClassDefinition(schemeObj)
        
        methodString = "";
        self.memberVariables = ""
        for prop in schemeObj.props:
            methodString += self.getMethod(schemeObj, prop)

        for variable in self.memberVariables.split("\n"):
            if len(variable) > 0:
                sourceString += self.indent(1) + variable + ";"

        sourceString += "\n"

        setterString = "";
        getterString = "";
        for variable in self.memberVariables.split("\n"):
            setterString += self.createSetter(variable)
            getterString += self.createGetter(variable)

        sourceString += self.getConstructor(schemeObj)
        sourceString += setterString
        sourceString += getterString

        # end class body
        sourceString += "}\n"

        if not os.path.exists(self.dirPath + "/internal"):
            os.makedirs(self.dirPath + "/internal")
        try:
            sourceFile = open(self.dirPath + "/internal/" + self.getClassName(schemeObj) + ".java", "w")
            sourceFile.write(sourceString) # Write a string to a file
        finally:
            sourceFile.close()

    def makeExtension(self, schemeObj):
        sourceString = ""
        self.isChild = False;
        self.isAbstract = False
        print "extending: " + self.getClassName(schemeObj)

        if len(self.dirPath) > 0:
            sourceString += "package " + self.dirPath.replace("/", ".") + ";\n\n"
        sourceString += self.getCommonDescriptionString()
        sourceString += self.getImports(schemeObj)
        sourceString += "import " + self.dirPath.replace("/", ".") + ".internal.Abstract" + self.getClassName(schemeObj) + ";\n"
        
        sourceString += "\npublic class " + self.getClassName(schemeObj)
        sourceString += " extends Abstract" + self.getClassName(schemeObj)
        sourceString += " {\n"
        
        sourceString += self.indent(1) + "public " + self.getClassName(schemeObj) + "(JSONObject json) throws JSONException {"
        sourceString += self.indent(2) + "super(json);"
        sourceString += self.indent(1) + "}\n"
        # end class body
        sourceString += "}\n"
        try:
            sourceFile = open(self.dirPath + "/" + self.getClassName(schemeObj) + ".java", "w")
            sourceFile.write(sourceString) # Write a string to a file
        finally:
            sourceFile.close()

    def getClassDefinition(self, schemeObj):
        abstract = ""
        classDef = "\npublic class " + self.getClassName(schemeObj)
        if self.isAbstract is True:
            abstract = "Abstract"
            classDef = "\npublic abstract class " + self.getClassName(schemeObj)
        if schemeObj.base_type != "object":
            self.isChild = True
            classDef += " extends " + abstract + self.projectPrefix + self.cap(schemeObj.base_type)
        classDef += " {\n"
        return classDef

    def getMethod(self, schemeObj, prop=None):
        source = ""
        if len(prop.getBaseTypes()) == 0:
            # only one base type
            source += self.getMethodForBaseType(schemeObj, prop, prop.base_type)
        else:
            # multiple base types
            for baseType in prop.getBaseTypes():
                if schemeObj.hasScheme(baseType):
                    baseTypeScheme = schemeObj.getScheme(baseType)
                    objectName = self.convertToJavaType(baseTypeScheme.type_name)
                    className = self.projectPrefix + self.cap(self.convertToJavaType(baseTypeScheme.type_name))
                    if len(baseTypeScheme.getBaseTypes()) == 0:
                        if self.convertToJavaType(baseTypeScheme.base_type) == "array":
                            for subType in baseTypeScheme.sub_type:
                                className = self.cap(subType)
                                projectPrefix = ""
                                if schemeObj.hasScheme(subType) and len(schemeObj.getScheme(subType).props) > 0:
                                    projectPrefix = self.projectPrefix
                                
                                self.addOrIgnoreMemberVariable("private", "ArrayList<" + projectPrefix + className + ">", self.getVariableName(prop.type_name) + "As" + className)
                                if prop.required is True:
                                    source += self.indent(2) + "final JSONArray " + self.getVariableName(prop.type_name) + "As" + className + "Array = json.getJSONArray(\"" + self.getVariableName(prop.type_name) + "\");"
                                else:
                                    extraIndent = "    "
                                    source += self.indent(2) + "final JSONArray " + self.getVariableName(prop.type_name) + "As" + className + "Array = json.optJSONArray(\"" + self.getVariableName(prop.type_name) + "\");"
                                    source += self.indent(2) + "if (" + self.getVariableName(prop.type_name) + "As" + className + "Array == null) {"
                                    source += self.indent(3) + self.getVariableName(prop.type_name) + "As" + className + " = null;"
                                    source += self.indent(2) + "} else {"

                                source += self.indent(2) + extraIndent + self.getVariableName(prop.type_name) + "As" + className + " = new ArrayList<" + projectPrefix + className + ">(" + self.getVariableName(prop.type_name) + "As" + className + "Array.length());"
                                source += self.indent(2) + extraIndent + "for (int i = 0; i < " + self.getVariableName(prop.type_name) + "As" + className + "Array.length(); i++) {"
                                if self.isNatural(className):
                                    source += self.indent(3) + extraIndent + self.getVariableName(prop.type_name) + "As" + className + ".add(" + self.getVariableName(prop.type_name) + "As" + className + "Array.get" + className + "(i));"
                                else:
                                    source += self.indent(3) + extraIndent + self.getVariableName(prop.type_name) + "As" + className + ".add(new " + projectPrefix + className + "(" + self.getVariableName(prop.type_name) + "As" + className + "Array.getJSONObject(i)));"
                                source += self.indent(2) + extraIndent + "}"
                                source += self.indent(2) + "}"
                            return source
                        variableName = self.getVariableName(prop.type_name) + "As" + self.cap(objectName)
                        self.addOrIgnoreMemberVariable("private", self.cap(className), variableName)
                        getType = "opt"
                        if prop.required is True:
                            getType = "get"

                        if self.isNatural(className):
                            source += self.getSchemeLimitationBody(schemeObj, baseTypeScheme)
                        else:
                            source += self.indent(2) + variableName + " = new " + self.projectPrefix + self.cap(self.convertToJavaType(baseTypeScheme.type_name)) + "(json.getJSONObject(\"" + self.getVariableName(prop.type_name) + "\"));"
                    else:
                        asString = ""
                        if self.convertToJavaType(baseTypeScheme.base_type) == "multi":
                            asString = "As" + className
                        projectPrefix = ""
                        if baseTypeScheme.isNaturalType() is False:
                            projectPrefix = self.projectPrefix

                        self.addOrIgnoreMemberVariable("private", projectPrefix + className, self.getVariableName(prop.type_name) + asString)
                        if prop.required is True:
                            source += self.indent(2) + self.getVariableName(prop.type_name) + " = new " + projectPrefix + className + "(json.getJSONObject(\"" + self.getVariableName(prop.type_name) + "\"));"
                        else:
                            source += self.indent(2) + "final JSONObject " + self.getVariableName(prop.type_name) + "JsonObject = json.optJSONObject(\"" + self.getVariableName(prop.type_name) + "\");"
                            source += self.indent(2) + "if (" + self.getVariableName(prop.type_name) + "JsonObject == null) {"
                            source += self.indent(3) + "return null;"
                            source += self.indent(2) + "} else {"
                            source += self.indent(3) + self.getVariableName(prop.type_name) + " = new " + projectPrefix + className + "(" + self.getVariableName(prop.type_name) + "JsonObject);"
                            source += self.indent(2) + "}"
                else:
                    className = self.convertToJavaType(baseType)
                    variableName = self.getVariableName(prop.type_name) + "As" + self.cap(className)
                    if self.low(className) == "byte":
                        self.addOrIgnoreMemberVariable("private", "byte[]", variableName)
                    else:
                        self.addOrIgnoreMemberVariable("private", self.cap(className), variableName)
                    
                    getType = "opt"
                    if prop.required is True:
                        getType = "get"

                    if self.isNatural(baseType):
                        source += self.indent(2) + variableName + " = json." + getType + self.cap(className) + "(\"" + self.getVariableName(prop.type_name) + "\");"
                    else:
                        if self.low(className) == "date":
                            source += self.indent(2) + variableName + " = new Date(json." + getType + "Long(\"" + self.getVariableName(prop.type_name) + "\"));"
                        elif self.low(className) == "byte":
                            source += self.indent(2) + variableName + " = json." + getType + "String(\"" + self.getVariableName(prop.type_name) + "\").getBytes();"
                        else:
                            source += self.indent(2) + variableName + " = json." + getType + self.cap(className) + "(\"" + self.getVariableName(prop.type_name) + "\");"
        return source

    def getSchemeLimitationBody(self, schemeObj, prop):
        className = self.convertToJavaType(prop.base_type)
        varName = self.getVariableName(prop.type_name)
        source = self.indent(2) + varName + " = json.get" + className + "(\"" + varName + "\");"
        if prop.base_type == "array":
            if prop.hasMaxCount:
                source += self.indent(2) + "if (" + varName + ".length < " + str(prop.minCount) + ") {"
                source += self.indent(3) + "throw new IllegalArgumentException(\"" + varName + " can't be less than " + str(prop.minCount) + "\");"
                source += self.indent(2) + "}"
            if prop.hasMaxCount:
                source += self.indent(2) + "if (" + varName + ".length > " + str(prop.maxCount) + ") {"
                source += self.indent(3) + "throw new IllegalArgumentException(\"" + varName + " can't be bigger than " + str(prop.maxCount) + "\");"
                source += self.indent(2) + "}"
        if prop.hasMinLength:
            source += self.indent(2) + "if (" + varName + ".length() < " + str(prop.minLength) + ") {"
            source += self.indent(3) + "throw new IllegalArgumentException(\"" + varName + " can't be shorter than " + str(prop.minLength) + "\");"
            source += self.indent(2) + "}"
        if prop.hasMaxLength:
            source += self.indent(2) + "if (" + varName + ".length() > " + str(prop.maxLength) + ") {"
            source += self.indent(3) + "throw new IllegalArgumentException(\"" + varName + " can't be longer than " + str(prop.maxLength) + "\");"
            source += self.indent(2) + "}"
        if prop.regex:
            source += self.indent(2) + "if (!Pattern.compile(\"" + prop.regex + "\").matcher(" + varName + ").matches()) {"
            source += self.indent(3) + "throw new IllegalArgumentException(\"" + varName + " doesn't fit regex " + prop.regex + "\");"
            source += self.indent(2) + "}"

        source += self.indent(2) + "return " + varName + ";"
        return source

    def getMethodForBaseType(self, schemeObj, prop, typeName):
        source = ""
        baseType = typeName
        typeClassName = self.cap(self.convertToJavaType(typeName))
        if baseType == "array":
            for subType in prop.sub_type:
                objectName = self.convertToJavaType(subType)
                className = self.cap(objectName)
                projectPrefix = ""
                if schemeObj.hasScheme(subType) and len(schemeObj.getScheme(subType).props) > 0:
                    projectPrefix = self.projectPrefix

                variableName = self.getVariableName(prop.type_name) + "As" + self.cap(subType)

                self.addOrIgnoreMemberVariable("private", "ArrayList<" + projectPrefix + className + ">", variableName)
                extraIndent = ""
                if prop.required is True:
                    source += self.indent(2) + "final JSONArray " + variableName + "Array = json.getJSONArray(\"" + self.getVariableName(prop.type_name) + "\");"
                else:
                    extraIndent = "    "
                    source += self.indent(2) + "final JSONArray " + variableName + "Array = json.optJSONArray(\"" + self.getVariableName(prop.type_name) + "\");"
                    source += self.indent(2) + "if (" + variableName + "Array == null) {"
                    source += self.indent(3) + variableName + " = null;"
                    source += self.indent(2) + "} else {"

                source += self.indent(2) + extraIndent + variableName + " = new ArrayList<" + projectPrefix + className + ">(" + variableName + "Array.length());"
                source += self.indent(2) + extraIndent + "for (int i = 0; i < " + variableName + "Array.length(); i++) {"
                if self.isNatural(className):
                    if className == "Object":
                        className = ""
                    source += self.indent(3) + extraIndent + variableName + ".add(" + variableName + "Array.get" + className + "(i));"
                else:
                    source += self.indent(3) + extraIndent + variableName + ".add(new " + projectPrefix + className + "(" + variableName + "Array.getJSONObject(i)));"
                source += self.indent(2) + extraIndent + "}"
                source += self.indent(2) + "}"
        elif baseType == "date":
            self.addOrIgnoreMemberVariable("private", self.cap(self.convertToJavaType(prop.rootBaseType())), self.getVariableName(prop.type_name))
            if prop.required is True:
                source += self.indent(2) + self.getVariableName(prop.type_name) + " = new Date(json.getInt(\"" + self.getVariableName(prop.type_name) + "\") / 1000);"
            else:
                source += self.indent(2) + "final int " + self.getVariableName(prop.type_name) + "Timestamp = json.optInt(\"" + self.getVariableName(prop.type_name) + "\", -1);"
                source += self.indent(2) + "if (" + self.getVariableName(prop.type_name) + "Timestamp == -1) {"
                source += self.indent(3) + self.getVariableName(prop.type_name) + " = null;"
                source += self.indent(2) + "} else {"
                source += self.indent(3) + self.getVariableName(prop.type_name) + " = new Date(" + self.getVariableName(prop.type_name) + "Timestamp / 1000);"
                source += self.indent(2) + "}"
        else:
            if self.isNatural(prop.rootBaseType()) is True:
                self.addOrIgnoreMemberVariable("private", self.cap(self.convertToJavaType(prop.rootBaseType())), self.getVariableName(prop.type_name))
                getMethod = typeClassName
                if getMethod == "Object":
                    getMethod = "" # reset as the getter for Object is just json.get()
                if prop.required is True:
                    source += self.indent(2) + self.getVariableName(prop.type_name) + " = json.get" + getMethod + "(\"" + self.getVariableName(prop.type_name) + "\");"
                else:
                    if len(getMethod) == 0:
                        source += self.indent(2) + self.getVariableName(prop.type_name) + " = json.opt" + getMethod + "(\"" + self.getVariableName(prop.type_name) + "\");"
                    else:
                        source += self.indent(2) + self.getVariableName(prop.type_name) + " = json.opt" + getMethod + "(\"" + self.getVariableName(prop.type_name) + "\", " + str(self.getDefaultValue(typeClassName)) + ");"
            else:
                self.addOrIgnoreMemberVariable("private", self.projectPrefix + self.cap(typeName), self.getVariableName(prop.type_name))
                typeName = self.convertToJavaType(prop.base_type);
                if prop.required is True:
                    source += self.indent(2) + self.getVariableName(prop.type_name) + " = new " + self.projectPrefix + self.cap(typeName) + "(json.getJSONObject(\"" + self.getVariableName(prop.type_name) + "\"));"
                else:
                    source += self.indent(2) + "final JSONObject " + self.getVariableName(prop.type_name) + "Json = json.optJSONObject(\"" + self.getVariableName(prop.type_name) + "\");"
                    source += self.indent(2) + "if (" + self.getVariableName(prop.type_name) + "Json == null) {"
                    source += self.indent(3) + self.getVariableName(prop.type_name) + " = null;"
                    source += self.indent(2) + "} else {"
                    source += self.indent(3) + self.getVariableName(prop.type_name) + " = new " + self.projectPrefix + self.cap(typeName) + "(" + self.getVariableName(prop.type_name) + "Json);"
                    source += self.indent(2) + "}"

        return source

    def getImports(self, schemeObj):
        source = "\nimport org.json.JSONObject;"
        source += "\nimport org.json.JSONArray;"
        source += "\nimport org.json.JSONException;"
        source += "\nimport java.util.ArrayList;"
        source += "\nimport java.util.Date;" # somehow date will not be added later - temporary static import
        source += "\nimport " + self.dirPath.replace("/", ".") + ".*;"
        source += "\n\nimport java.lang.IllegalArgumentException;\n"
        stringImported = False
        dateImported = False
        regexImported = False
        for prop in schemeObj.props:
            baseTypes = schemeObj.getScheme(schemeObj.getScheme(prop.type_name).type_name).getBaseTypes()
            if prop.base_type == "string" and stringImported is False:
                source += "import java.lang.String;\n"
                stringImported = True
            if prop.base_type == "date" and dateImported is False:
                source += "import java.util.Date;\n"
                dateImported = True
            for baseType in baseTypes:
                if not schemeObj.hasScheme(baseType):
                    continue
                else:
                    base = schemeObj.getScheme(baseType)
                    if len(base.regex) > 0 and regexImported is False:
                        source += "import java.util.regex.Pattern;\n"
                        regexImported = True
        return source

    def getConstructor(self, schemeObj):
        source = self.indent(1) + "public " + self.cap(self.getClassName(schemeObj)) + "(JSONObject json) throws JSONException {"
        if self.isChild:
            source += self.indent(2) + "super(json);"
        else:
            source += self.indent(2) + "if (json == null) {"
            source += self.indent(3) + "throw new IllegalArgumentException(\"JSONObject can't be null\");"
            source += self.indent(2) + "}"
        for prop in schemeObj.props:
            source += self.getMethod(schemeObj, prop)
        source += self.indent(1) + "}\n"
        return source

    ### helper methods
    def cap(self, name):
        return name[0].capitalize() + name[1:]

    def low(self, name):
        return name[0].lower() + name[1:]

    def indent(self, size):
        i = 0
        indent = "\n"
        while i < size:
            indent += "    "
            i += 1
        return indent

    def convertToJavaType(self, objCType):
        if objCType == "number":
            return "double"
        elif objCType == "any":
            return "Object"
        elif objCType == "data":
            return "byte"
        elif objCType == "string":
            return "String"
        elif objCType == "date":
            return "Date"
        else:
            return objCType

    def isNatural(self, objectType):
        objectType = self.convertToJavaType(objectType)
        return objectType in self.naturalList

    def getDefaultValue(self, type):
        typeName = self.low(self.convertToJavaType(type))
        if typeName == "double":
            return 0
        elif typeName == "boolean":
            return "false"
        return "null"

    def addOrIgnoreMemberVariable(self, visibility, type, name):
        newVariable = visibility + " " + type + " " + name + ""
        
        if not newVariable in self.memberVariables.split("\n"):
            self.memberVariables += newVariable + "\n"

    def createMethodHead(self, visibility, returnType, name, parameter = ""):
        return self.indent(1) + visibility + " " + returnType + " " + name + "(" + parameter + ") {"

    def createSetter(self, variableString):
        elements = variableString.split(" ")
        if len(elements) == 3:
            source = self.createMethodHead("public", "void", "set" + self.cap(elements[2]), elements[1] + " " + self.low(elements[2]))
            source += self.indent(2) + "this." + elements[2] + " = " + self.low(elements[2]) + ";"
            source += self.indent(1) + "}\n"
            return source
        return ""

    def createGetter(self, variableString):
        elements = variableString.split(" ")
        if len(elements) == 3:
            source = self.createMethodHead("public", elements[1], "get" + self.cap(elements[2]))
            source += self.indent(2) + "return " + elements[2] + ";"
            source += self.indent(1) + "}\n"
            return source
        return ""

    def getClassName(self, schemeObj):
        if self.isAbstract is True:
            return "Abstract" + schemeObj.getClassName()
        else:
            return schemeObj.getClassName()

    def getVariableName(self, name):
        if name in ["private", "protected", "public", "class", "abstract", "final", "static"]:
            return self.projectPrefix + self.cap(name)
        return name