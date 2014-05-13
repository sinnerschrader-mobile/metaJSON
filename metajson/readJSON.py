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

__version__ = "2.7.2"

import json
import os
import glob
import shutil
import sys, getopt

from JSONScheme import *
from ObjectiveCCodeGenerator import *
from JavaCodeGenerator import *

def main(argv=sys.argv):
    jsonfiles = []
    inputfile = 'do you have files?'
    projectPrefix = ''
    target = 'iOS'
    dirPathToSaveCodes = './src'
    objectSuffix = "JSONObject"

    usageString = '\nreadJSON.py [ -p | -t | -o | -s ] [-i]\n'
    usageString += 'Options:\n'
    usageString += '  -h, --help            shows help\n'
    usageString += '  -p, --prefix=         project prefix (default: S2M)\n'
    usageString += '  -s, --suffix=         classname suffix (default: JSONObject). Use "-s false" for no suffix\n'
    usageString += '  -t, --target=         target platform iOS or Android (default: iOS)\n'
    usageString += '  -i, --input=          meta-JSON file to read\n'
    usageString += '  -o, --output=         ouput path of generated source codes\n'

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"ho:p:s:t:i:",["prefix=","suffix=","target=","input=","output="])
    except getopt.GetoptError:
        print(usageString)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(usageString)
            sys.exit()
        elif opt in ("-p", "--prefix"):
            projectPrefix = arg
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            dirPathToSaveCodes = arg
        elif opt in ("-s", "--suffix"):
            objectSuffix = arg
            if objectSuffix == "false":
                objectSuffix = ""

    addFiles = False
    for arg in argv :
        if arg.endswith(inputfile) :
            jsonfiles.append(inputfile)
            addFiles = True
            continue

        if arg.startswith('-') and addFiles :
            addFiles = False
            break

        if addFiles :
            jsonfiles.append(arg)

    if target == 'none' :
        print 'error - target platform is not defined'
        print(usageString)
        sys.exit()

    if len(jsonfiles) == 0 :
        print 'error - meta JSON file is not defined'
        print(usageString)
        sys.exit()

    if not os.path.exists(dirPathToSaveCodes):
        os.makedirs(dirPathToSaveCodes)

    iOS = False
    Android = False
    if target == 'iOS' :
        iOS = True
    elif target == 'Android' :
        Android = True
    else :
        print 'error - unknown target platform : ' + target
        print(usageString)
        sys.exit()

    hasError = False

    if iOS :
        if dirPathToSaveCodes.endswith("/") :
                dirPathToSaveCodes = dirPathToSaveCodes[:-1]

        if os.path.exists(dirPathToSaveCodes + "/AbstractInterfaceFiles"):
            shutil.rmtree(dirPathToSaveCodes + "/AbstractInterfaceFiles")

        templateCodeGen = TemplateCodeGenerator()
        templateCodeGen.projectPrefix = projectPrefix
        templateCodeGen.dirPath = dirPathToSaveCodes
        templateCodeGen.writeTemplates()

    JSONScheme.projectPrefix = projectPrefix
    JSONScheme.objectSuffix = objectSuffix

    print "\nGenerate source codes for " + target + ", with Project Prefix \'" + projectPrefix + "\' and suffix \'" + objectSuffix + "\'"
    print "Output path : \'" + dirPathToSaveCodes + "\'\n"

    for filePath in jsonfiles :
        print "read " + filePath + " to parse ...."

        jsonObj = openFileAndParseJSON(filePath)

        if type(jsonObj) == list :
            for dic in jsonObj :
                schemeObj = JSONScheme()
                schemeObj.projectPrefix = projectPrefix
                schemeObj.objectSuffix = objectSuffix
                if schemeObj.parseDictionary(dic) == False:
                    hasError = True
                    break

        elif type(jsonObj) == dict :
            schemeObj = JSONScheme()
            if schemeObj.parseDictionary(jsonObj) == False :
                hasError = True

        else :
            hasError = True
            print "error : no JSON Scheme"
            break;

        if hasError :
            print "error - Fail to make scheme object."
            break;

        if hasError :
            break

        if not hasError:
            codeGen = 0

            if Android :
                codeGen = JavaCodeGenerator()
            else :
                codeGen = ObjectiveCCodeGenerator()

            codeGen.projectPrefix = projectPrefix
            codeGen.dirPath = dirPathToSaveCodes
            codeGen.objectSuffix = objectSuffix
            allSchemes = JSONScheme.JSONSchemeDic
            codeGen.JSONSchemeDic = allSchemes

            rootDic = allSchemes["ROOT"]
            allRootKeys = rootDic.keys()
            for typeName in rootDic :
                obj = rootDic[typeName];
                if obj.isNaturalType() == False :
                    codeGen.make(obj)

def openFileAndParseJSON(filePath):
    f = open(filePath)

    try:
        obj = json.load(f)
    finally:
        f.close()

    return obj

def version():
    print("Running metajson version %s." % __version__)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
