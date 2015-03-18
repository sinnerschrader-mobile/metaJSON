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

__version__ = "1.0.0"

import yaml

import json
import os
import glob
import shutil
import sys, getopt

from JSONScheme import *
from SourceCodeGenerator import *

def main(argv=sys.argv):
    # parse Options
    template_dir = None
    packageName = ""
    jsonfiles = []
    inputfile = 'do you have files?'
    projectPrefix = 'S2M'
    dirPathToSaveCodes = './src'
    objectSuffix = "JSONObject"

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"vhp:s:i:o:",["version", "help", "prefix=", "suffix=", "input=", "output=", "template=", "package="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--version"):
            version()
        elif opt in ("-p", "--prefix"):
            projectPrefix = arg
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            dirPathToSaveCodes = arg
        elif opt in ("-s", "--suffix"):
            objectSuffix = arg
            if objectSuffix == "false":
                objectSuffix = ""
        elif opt in ("--template"):
            template_dir = arg
        elif opt in ("--package"):
            packageName = arg
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

    if len(jsonfiles) == 0 :
        print 'error - meta JSON file is not defined'
        usage()

    if not os.path.exists(dirPathToSaveCodes):
        os.makedirs(dirPathToSaveCodes)

    hasError = False

    print "\nGenerate source codes with Project Prefix \'" + projectPrefix + "\' and suffix \'" + objectSuffix + "\'"
    print "Output path : \'" + dirPathToSaveCodes + "\'\n"

    # write templates
    if dirPathToSaveCodes.endswith("/") :
            dirPathToSaveCodes = dirPathToSaveCodes[:-1]

    if template_dir == None:
        template_dir = os.path.join(TemplateCodeGenerator.DEFAULT_TEMPLATE_PATH, "iOS")

    templateCodeGen = TemplateCodeGenerator(template_dir, dirPathToSaveCodes, projectPrefix, packageName)
    templateCodeGen.write_general_template_files()


    # read JSON file
    JSONScheme.projectPrefix = projectPrefix
    JSONScheme.packageName = packageName
    JSONScheme.objectSuffix = objectSuffix
    for filePath in jsonfiles :
        print "read " + filePath + " to parse ...."
        jsonObj = read_file(filePath)
        schemeObj = create_json_scheme(jsonObj)

        codeGen = SourceCodeGenerator()
        allSchemes = JSONScheme.JSONSchemeDic
        rootDic = allSchemes["ROOT"]
        for typeName in rootDic :
            obj = rootDic[typeName];
            if obj.isNaturalType() == False:
                for template_filename in templateCodeGen.json_template_files:
                    template = open(template_filename)
                    content = codeGen.render(obj, template.read())
                    file = templateCodeGen.create_template_output_file(template_filename, obj.getClassName())
                    try:
                        file.write(content)
                    finally :
                        file.close()



def create_json_scheme(jsonObj):
    schemeObj = None
    if type(jsonObj) == list :
        for dic in jsonObj :
            schemeObj = JSONScheme()
            if schemeObj.parseDictionary(dic) == False:
                schemeObj = None
                print "error - Fail to make scheme object."
                break

    elif type(jsonObj) == dict :
        schemeObj = JSONScheme()
        if schemeObj.parseDictionary(jsonObj) == False :
            schemeObj = None
            print "error - Fail to make scheme object."
    else :
        print "error : no JSON Scheme"
    return schemeObj

def usage():
    usageString = 'Options:\n'
    usageString += '  -v, --version         shows version\n'
    usageString += '  -h, --help            shows help\n'
    usageString += '  -p, --prefix=         project prefix (default: S2M)\n'
    usageString += '  -s, --suffix=         classname suffix (default: JSONObject). Use "-s false" for no suffix\n'
    usageString += '  -i, --input=          metaJSON file to read\n'
    usageString += '  -o, --output=         output path of generated source codes (default: src)\n'
    usageString += '      --template=       template directory to use to generate code\n'
    usageString += '      --package=        name of the generated package (default: none)\n'
    print(usageString)
    sys.exit()

def read_file(file_path):
    basename, extension = os.path.splitext(file_path)
    if extension == '.yaml':
        return open_yaml_file(file_path)
    else:
        return openFileAndParseJSON(file_path)

"Opens and read content of yaml file"
def open_yaml_file(file_path):
    f = open(file_path)
    try:
        obj = yaml.load(f)
    finally:
        f.close()
    return obj

"Opens and read content of json file"
def openFileAndParseJSON(filePath):
    f = open(filePath)
    try:
        obj = json.load(f)
    finally:
        f.close()
    return obj

def git_revision_short_hash():
    import subprocess
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

def version():
    git_rev = git_revision_short_hash()
    if git_rev:
        print("metaJSON version {}. git revision {}").format(__version__, git_rev)
    else:
        print("metaJSON version %s." % __version__)
    sys.exit(0)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
