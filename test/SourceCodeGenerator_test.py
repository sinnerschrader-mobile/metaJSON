from metajson.SourceCodeGenerator import SourceCodeGenerator
from metajson.JSONScheme import *

import pickle
import unittest
import sys
import os
import datetime

class TestSourceCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SourceCodeGenerator()
        self.maxDiff = None
        self.default_folder = 'test/data/'

    def tearDown(self):
        del self.gen

    def template_file_path(self, filename) :
        templatePath = os.path.realpath( __file__ )
        templatePath = templatePath.replace(os.path.basename( __file__ ), '../metajson/templates/iOS')
        return os.path.join(templatePath, filename)

    def human_header_content(self, schemeObj) :
        template_file = open(self.template_file_path("_CLASSNAME_.h.mustache"), "r")
        return self.gen.render(schemeObj, template_file.read())

    def human_source_content(self, schemeObj) :
        template_file = open(self.template_file_path("_CLASSNAME_.m.mustache"), "r")
        return self.gen.render(schemeObj, template_file.read())

    def machine_header_content(self, schemeObj) :
        template_file = open(self.template_file_path("AbstractInterfaceFiles/__CLASSNAME_.h.mustache"), "r")
        return self.gen.render(schemeObj, template_file.read())

    def machine_source_content(self, schemeObj) :
        template_file = open(self.template_file_path("AbstractInterfaceFiles/__CLASSNAME_.m.mustache"), "r")
        return self.gen.render(schemeObj, template_file.read())

    def assert_content_file(self, filename, content):
        with open(filename, 'r') as content_file:
            expected_result = content_file.read()
        # All reference files have a timestamp of 2014 so we tweak our generated code to match them.
        self.assertMultiLineEqual(content.replace(str(datetime.datetime.now().year), "2014"), expected_result)

class TestSampleTestClassCase(TestSourceCodeGenerator):
    def setUp(self):
        super(TestSampleTestClassCase, self).setUp()
        self.test_file_path = self.default_folder + 'test_class'
        self.scheme_object = pickle.load(open(self.test_file_path + '.p', 'rb'))


    def test_human_header_content(self):
        result = self.human_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/S2MSenderJSONObject.h", result)

    def test_human_source_content(self):
        result = self.human_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/S2MSenderJSONObject.m", result)

    def test_machine_source_content(self):
        result = self.machine_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MSenderJSONObject.m", result)

    def test_machine_header_content(self):
        result = self.machine_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MSenderJSONObject.h", result)


class TestSampleTestStringOptionsCase(TestSourceCodeGenerator):
    def setUp(self):
        super(TestSampleTestStringOptionsCase, self).setUp()
        self.test_file_path = self.default_folder + 'test_string_options'
        self.scheme_object = pickle.load(open(self.test_file_path + '.p', 'rb'))

    def test_machine_source_content(self):
        result = self.machine_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MLoginJSONObject.m", result)

    def test_machine_header_content(self):
        result = self.machine_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MLoginJSONObject.h", result)

class TestSampleTestSubclassCase(TestSourceCodeGenerator):
    def setUp(self):
        super(TestSampleTestSubclassCase, self).setUp()
        scheme = pickle.load(open(self.default_folder + '/test_subclass_scheme.p', 'rb'))
        JSONScheme.JSONSchemeDic = scheme


class TestSampleTestSubclassMotherCase(TestSampleTestSubclassCase):
    def setUp(self):
        super(TestSampleTestSubclassMotherCase, self).setUp()
        self.test_file_path = self.default_folder + 'test_subclass'
        self.scheme_object = pickle.load(open(self.default_folder + '/test_subclass_motherClass.p', 'rb'))

    def test_human_header_content(self):
        result = self.human_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/MotherClassJSONObject.h", result)

    def test_human_source_content(self):
        result = self.human_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/MotherClassJSONObject.m", result)

    def test_machine_source_content(self):
        result = self.machine_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_MotherClassJSONObject.m", result)

    def test_machine_header_content(self):
        result = self.machine_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_MotherClassJSONObject.h", result)

class TestSampleTestSubclassSubclassCase(TestSampleTestSubclassCase):
    def setUp(self):
        super(TestSampleTestSubclassSubclassCase, self).setUp()
        self.test_file_path = self.default_folder + 'test_subclass'
        self.scheme_object = pickle.load(open(self.default_folder + '/test_subclass_subClass.p', 'rb'))

    def test_human_header_content(self):
        result = self.human_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/SubClassJSONObject.h", result)

    def test_human_source_content(self):
        result = self.human_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/SubClassJSONObject.m", result)

    def test_machine_source_content(self):
        result = self.machine_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_SubClassJSONObject.m", result)

    def test_machine_header_content(self):
        result = self.machine_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_SubClassJSONObject.h", result)

class TestSampleTestTypesCase(TestSourceCodeGenerator):
    def setUp(self):
        super(TestSampleTestTypesCase, self).setUp()
        scheme = pickle.load(open(self.default_folder + '/test_types_scheme.p', 'rb'))
        JSONScheme.JSONSchemeDic = scheme

        self.test_file_path = self.default_folder + 'test_types'
        self.scheme_object = pickle.load(open(self.default_folder + '/test_types_superObject.p', 'rb'))

    def test_machine_header_content(self):
        result = self.machine_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MSuperObjectJSONObject.h", result)

    def test_machine_source_content(self):
        result = self.machine_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MSuperObjectJSONObject.m", result)


if __name__ == '__main__':
    unittest.main()
