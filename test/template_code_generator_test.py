import unittest
import os

from metajson.template_code_generator import *


class TestTemplateCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.object = TemplateCodeGenerator()

    def test_read_template(self):
        expected_jsons = ['./metajson/templates/_header.h.mustache', './metajson/templates/_source.m.mustache', './metajson/templates/header.h.mustache', './metajson/templates/source.m.mustache']
        expected_api_templates = ['./metajson/templates/APIParser/APIParser.h', './metajson/templates/APIParser/APIParser.m', './metajson/templates/Utilities/NSString+RegExValidation.h', './metajson/templates/Utilities/NSString+RegExValidation.m']

        self.object.read_template()

        self.assertEqual(self.object.json_template_files,expected_jsons)
        self.assertEqual(self.object.general_template_files,expected_api_templates)
