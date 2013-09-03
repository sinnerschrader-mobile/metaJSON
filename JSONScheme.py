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

class JSONScheme :
    JSONSchemeDic = {}
    naturalTypeList = ['string', 'array', 'date', 'data', 'boolean', 'number']
    projectPrefix = ""
    objectSuffix = "JSONObject"
    type_name = ""
    key_name = ""
    base_type = ""
    base_type_list = []
    type_description = ""
    sub_type = []
    props = []
    regex = ""
    hasMaxCount = False
    hasMinCount = False
    hasMaxValue = False
    hasMinValue = False
    hasMaxLength = False
    hasMinLength = False
    required = False
    
    maxCount = 0
    minCount = 0
    maxValue = 0
    minValue = 0
    maxLength = 0
    minLength = 0
    
    domain = ["ROOT"]

    def __init__(self):
        projectPrefix = ""
        objectSuffix = "JSONObject"
        type_name = ""
        key_name = ""
        base_type = ""
        base_type_list = []
        type_description = ""
        sub_type = ["any"]
        props = []
        regex = ""
        hasMaxCount = False
        hasMinCount = False
        hasMaxValue = False
        hasMinValue = False
        hasMaxLength = False
        hasMinLength = False
        required = False
        maxCount = 0
        minCount = 0
        maxValue = 0
        minValue = 0
        maxLength = 0
        minLength = 0
        domain = ["ROOT"]
    
    def hasScheme(self, schemeName) :
        tmpDomainList = list(self.domain)
        tmpDomainList.append(self.type_name)
        #print "find : " + schemeName + ", at : " + str(tmpDomainList)
        
        for nn in range(0,len(tmpDomainList)) :
            tmpDomainKey = ""
            for mm in range(0,len(tmpDomainList) - nn) :
                tmpDomainKey += str(tmpDomainList[mm])
            
            if JSONScheme.JSONSchemeDic.has_key(tmpDomainKey) :
                tmpDomainDic = JSONScheme.JSONSchemeDic[tmpDomainKey]
                if tmpDomainDic.has_key(schemeName) :
                    #print "Found : " + schemeName
                    #print "==============================================="
                    return True

        #print "Not Found : " + schemeName
        #print "==============================================="
        return False

    def getScheme(self, schemeName) :
        tmpDomainList = list(self.domain)
        tmpDomainList.append(self.type_name)
        for nn in range(0,len(tmpDomainList)) :
            tmpDomainKey = ""
            for mm in range(0,len(tmpDomainList) - nn) :
                tmpDomainKey += str(tmpDomainList[mm])
            
            if JSONScheme.JSONSchemeDic.has_key(tmpDomainKey) :
                tmpDomainDic = JSONScheme.JSONSchemeDic[tmpDomainKey]
                if tmpDomainDic.has_key(schemeName) :
                    return tmpDomainDic[schemeName]


        return False
    
    def getDomainString(self) :
        domainString = ""
        for index in range(0, len(self.domain)) :
            domainString += self.domain[index]
            if index in range(0,len(self.domain) - 1) :
                domainString += "."
        
        return domainString
    
    def getDomain(self) :
        domainString = ""
        for index in range(0, len(self.domain)) :
            domainString += self.domain[index]
        return domainString

    def setMaxValue(self, maxVal):
        self.maxValue = maxVal
        self.hasMaxValue = True
    
    def setMinValue(self, minVal):
        self.minValue = minVal
        self.hasMinValue = True
    
    def setMaxLength(self, maxLen):
        self.maxLength = maxLen
        self.hasMaxLength = True
    
    def setMinLength(self, minLen):
        self.minLength = minLen
        self.hasMinLength = True
    
    def setMaxCount(self, maxCnt):
        self.maxCount = maxCnt
        self.hasMaxCount = True
    
    def setMinCount(self, minCnt):
        self.minCount = minCnt
        self.hasMinCount = True
    
    def getMaxValue(self) :
        if self.hasMaxValue :
            return [True, self.maxValue]
        
        if self.base_type in self.naturalTypeList :
            return [False, 0];
        
        parentSchemeObj = self.getScheme(self.base_type)
        
        return parentSchemeObj.getMaxValue()
    
    def getMinValue(self) :
        if self.hasMinValue :
            return [True, self.minValue]
    
        if self.base_type in self.naturalTypeList :
            return [False, 0];
        
        parentSchemeObj = self.getScheme(self.base_type)
        
        return parentSchemeObj.getMinValue()
    
    def getMaxCount(self) :
        if self.hasMaxCount :
            return [True, self.maxCount]
        
        if self.base_type in self.naturalTypeList :
            return [False, 0];
        
        parentSchemeObj = self.getScheme(self.base_type)
        
        return parentSchemeObj.getMaxCount()
    
    def getMinCount(self) :
        if self.hasMinCount :
            return [True, self.minCount]
        
        if self.base_type in self.naturalTypeList :
            return [False, 0];
        
        parentSchemeObj = self.getScheme(self.base_type)
        
        return parentSchemeObj.getMinCount()
    
    def getMaxLength(self) :
        if self.hasMaxLength :
            return [True, self.maxLength]
        
        if self.base_type in self.naturalTypeList :
            return [False, 0];
        
        parentSchemeObj = self.getScheme(self.base_type)
        
        return parentSchemeObj.getMaxLength()
    
    def getMinLength(self) :
        if self.hasMinLength :
            return [True, self.minLength]
        
        if self.base_type in self.naturalTypeList :
            return [False, 0];
        
        parentSchemeObj = self.getScheme(self.base_type)
        
        return parentSchemeObj.getMinLength()
    
    def getRegex(self) :
        if len(self.regex) > 0 :
            return [True, self.regex]
        
        if self.base_type in self.naturalTypeList :
            return [False, 0];
        
        parentSchemeObj = self.getScheme(self.base_type)

        if parentSchemeObj :
            return parentSchemeObj.getRegex()
        else :
            return [False, 0];
    
    def getClassName(self):
        
        if len(self.props) or self.base_type == "object" :
            className = self.type_name.upper()
            className = self.projectPrefix + className[:1] + self.type_name[1:] + self.objectSuffix
            return className
        elif self.rootBaseType() == "object" :
            parentSchemeObj = self.getScheme(self.base_type)
            if parentSchemeObj :
                return parentSchemeObj.getClassName()

        print "error : " + self.type_name + " has no Class Name."
        return ""

    def getMachineClassName(self):
        
        if len(self.props) or self.rootBaseType() == "object" :
            className = self.type_name.upper()
            className = "_" + self.projectPrefix + className[:1] + self.type_name[1:] + self.objectSuffix
            return className

        print "error : " + self.type_name + " has no Class Name."
        return ""
    
    def rootBaseType(self) :
        if self.base_type in JSONScheme.naturalTypeList or self.base_type == "object" or self.base_type == "multi" or self.base_type == "any":
            return self.base_type
        else :
            if self.hasScheme(self.base_type) :
                parentTypeScheme = self.getScheme(self.base_type)
                return parentTypeScheme.rootBaseType()
                
        return self.base_type

    def isNaturalType(self) :
        
        root = self.rootBaseType()
        
        if root in JSONScheme.naturalTypeList :
            return True
                
        return False
    
    def canHaveProperty(self) :
        if self.rootBaseType() == "object" :
            return True

        return False
    
    def getSubType(self) :
        if self.isNaturalType() :
            return self.sub_type

        if len(self.sub_type) :
            return self.sub_type

        elif self.hasScheme(self.base_type) :
            parentTypeScheme = self.getScheme(self.base_type)
            return parentTypeScheme.getSubType()

        return self.sub_type
        
    def getBaseTypes(self) :
        
        if self.isNaturalType() :
            return self.base_type_list
        

        if len(self.base_type_list) :
            return self.base_type_list
        elif self.hasScheme(self.base_type) :
            parentTypeScheme = self.getScheme(self.base_type)
            return parentTypeScheme.getBaseTypes()

        return self.base_type_list

    """
        make new Scheme Object
    """
    
    def makeNewScheme(self, jsonDic):
        newScheme = JSONScheme()
        newScheme.projectPrefix = self.projectPrefix
        newScheme.objectSuffix = self.objectSuffix
        newScheme.domain = self.domain[:]
        newScheme.domain.append(self.type_name)
        #print newScheme.domain
        if newScheme.parseDictionary(jsonDic) :
            return newScheme

        return False


    """
        read Base Type
    """
    def parseBaseType(self, jsonObj) :
        if jsonObj == False :
            return False

        tmpList = []
        if type(jsonObj) == dict :
            newScheme = self.makeNewScheme(jsonObj)

            if newScheme :
                self.base_type = newScheme.type_name
            else :
                print "error - fail to make new type for base-type of ", self.type_name
                return False

        elif type(jsonObj) == list :
            self.base_type = "multi"
            for multiType in jsonObj :            
                if type(multiType) == dict :
                    newScheme = self.makeNewScheme(multiType)
                                
                    if newScheme :
                        tmpList.append(newScheme.type_name)
                    else :
                        print "error - fail to make new type for base-type(multi) of ", self.type_name
                        return False
                elif type(multiType) == list :
                    self.base_type = "any"
                    tmpList = []
                    return tmpList
                else :
                    multiType = str(multiType)
                    if multiType == "any" :
                        self.base_type = any
                        tmpList = []
                        return tmpList
                            
                    tmpList.append(multiType)
                
                    
        elif type(jsonObj) == str or type(jsonObj) == unicode:
            self.base_type = str(jsonObj)
    
        return tmpList

            
    """
    read sub type
    """
    def parseSubType(self, jsonObj) :
        tmpList = []
        if type(jsonObj) == dict :
            newScheme = self.makeNewScheme(jsonObj)
            
            if newScheme :
                tmpList.append(newScheme.type_name)
            else :
                print "error - fail to make new type for subType of ", self.type_name
                return False

        elif type(jsonObj) == list :
            for multiType in jsonObj :
                if type(multiType) == dict :
                    newScheme = self.makeNewScheme(multiType)
                    
                    if newScheme :
                        if newScheme.type_name in tmpList :
                            print "warning - ignore same type ("+ newScheme.type_name +") in subTypes of ", self.type_name
                        else :
                            tmpList.append(newScheme.type_name)
                    else :
                        print "error - fail to make new type for subType(multi) of ", self.type_name
                        return False
                elif type(multiType) == list :
                    tmpList = ["any"]
                    return tmpList
                else :
                    if str(multiType) == "any" :
                        tmpList = ["any"]
                        return tmpList
                    tmpList.append(str(multiType))

            
            
        else :
            if str(jsonObj) == "any" :
                tmpList = ["any"]
                return tmpList
            tmpList.append(str(jsonObj))

        return tmpList

    """
    read Property
    """
    def parseProperty(self, jsonObj) :
        tmpList = []
        if jsonObj and type(jsonObj) != list :
            print "Warning - ", self.type_name, " has no property."
            return tmpList

        for dic in jsonObj :
            newProp = self.makeNewScheme(dic)
            if newProp :
                tmpList.append(newProp)

        return tmpList

    """
        parse Scheme Object with Dic
    """
    def parseDictionary(self, jsonDic):
        if jsonDic.has_key('name') :
            self.type_name = str(jsonDic['name'])
        else :
            print "error - no type name : ", jsonDic
            return False

        # make domainKey
        tmpDomainKey = str(self.getDomain())

        if not JSONScheme.JSONSchemeDic.has_key(tmpDomainKey):
            JSONScheme.JSONSchemeDic[tmpDomainKey] = {}

        tmpDomainDic = JSONScheme.JSONSchemeDic[tmpDomainKey]
        if tmpDomainDic.has_key(self.type_name) :
            print "error - same type name is defined : " + self.type_name
            print "        same type name should not be defined in same level."
            return False

        tmpDomainDic[self.type_name] = self
        
        if jsonDic.has_key('base-type') :
            tmpBaseType = jsonDic['base-type']
            tmpBaseTypeList = self.parseBaseType(tmpBaseType)
            if tmpBaseTypeList == False:
                print "error - no base-type : ", self.type_name
                return False
            self.base_type_list = tmpBaseTypeList
        else :
            print "error - no base-type : ", self.type_name
            return False        
        
        if jsonDic.has_key('description') :
            self.type_description = str(jsonDic['description'])
        
        if jsonDic.has_key('required') :
            self.required = jsonDic['required']
        
        if jsonDic.has_key('maxValue') :
            self.setMaxValue(jsonDic['maxValue'])
        
        if jsonDic.has_key('minValue') :
            self.setMinValue(jsonDic['minValue'])
        
        if jsonDic.has_key('maxCount') :
            self.setMaxCount(jsonDic['maxCount'])
        
        if jsonDic.has_key('minCount') :
            self.setMinCount(jsonDic['minCount'])
        
        if jsonDic.has_key('maxLength') :
            self.setMaxLength(jsonDic['maxLength'])
        
        if jsonDic.has_key('minLength') :
            self.setMinLength(jsonDic['minLength'])
        
        if jsonDic.has_key('regex') :
            self.regex = str(jsonDic['regex'])

        tmpPropList = []
        
        if jsonDic.has_key('property') :
            tmpPropList = self.parseProperty(jsonDic['property'])
            if  tmpPropList == False :
                return False
            else :
                self.props = tmpPropList

        if jsonDic.has_key('subType') :
            tmpSubType = jsonDic['subType']
            tmpSubTypeList = self.parseSubType(tmpSubType)
            if tmpSubTypeList == False:
                return False
            self.sub_type = tmpSubTypeList
        
        if self.base_type == "array" and not jsonDic.has_key('subType') :
            print "warning - " + self.type_name + "(array type) has no subType. treat as any. "

        return True












