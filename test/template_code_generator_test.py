import unittest
import os

from metajson.template_code_generator import *


class TestTemplateCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.object = TemplateCodeGenerator("./metajson/templates/iOS")
        os.system("rm -rf ./classes")

    def test_read_template(self):
        expected_jsons = ['./metajson/templates/iOS/header.h.mustache', './metajson/templates/iOS/source.m.mustache', './metajson/templates/iOS/AbstractInterfaceFiles/_header.h.mustache', './metajson/templates/iOS/AbstractInterfaceFiles/_source.m.mustache']
        expected_api_templates = ['./metajson/templates/iOS/APIParser/_PREFIX_APIParser.h', './metajson/templates/iOS/APIParser/_PREFIX_APIParser.m', './metajson/templates/iOS/Utilities/NSString+RegExValidation.h', './metajson/templates/iOS/Utilities/NSString+RegExValidation.m']

        self.object.read_template()

        self.assertEqual(self.object.json_template_files,expected_jsons)
        self.assertEqual(self.object.general_template_files,expected_api_templates)

    def test_create_output_file(self):
        output = "classes/APIParser/S2MAPIParser.h"
        self.object.create_output_file("./metajson/templates/iOS/APIParser/_PREFIX_APIParser.h")
        file_exists = os.path.isfile(output) and os.access(output, os.R_OK)
        self.assertEqual(file_exists, True)

    def test_create_output_file_without_project_prefix(self):
        self.object.project_prefix = ""
        output = "classes/APIParser/APIParser.h"
        self.object.create_output_file("./metajson/templates/iOS/APIParser/_PREFIX_APIParser.h")
        file_exists = os.path.isfile(output) and os.access(output, os.R_OK)
        self.assertEqual(file_exists, True)

    # Uncomment for manual testing
    # def test_write_general_template_files(self):
    #     self.object.write_general_template_files()
