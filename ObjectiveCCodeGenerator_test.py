from ObjectiveCCodeGenerator import *
from JSONScheme import *

import pickle
import unittest


class TestObjectiveCCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ObjectiveCCodeGenerator()
        self.gen.dirPath = './src'
        self.maxDiff = None
        self.default_folder = 'test_data/'

    def tearDown(self):
        del self.gen

    def assert_content_file(self, filename, content):
        with open(filename, 'r') as content_file:
            expected_result = content_file.read()
        self.assertMultiLineEqual(content, expected_result)

class TestSampleTestClassCase(TestObjectiveCCodeGenerator):
    def setUp(self):
        super(TestSampleTestClassCase, self).setUp()
        self.test_file_path = self.default_folder + 'test_class'
        self.scheme_object = pickle.load(open(self.test_file_path + '.p', 'rb'))


    def test_human_header_content(self):
        result = self.gen.human_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/S2MSenderJSONObject.h", result)

    def test_human_source_content(self):
        result = self.gen.human_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/S2MSenderJSONObject.m", result)

    def test_machine_source_content(self):
        result = self.gen.machine_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MSenderJSONObject.m", result)

    def test_machine_header_content(self):
        result = self.gen.machine_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MSenderJSONObject.h", result)

class TestSampleTestCase(TestObjectiveCCodeGenerator):
    def setUp(self):
        super(TestSampleTestCase, self).setUp()
        self.test_file_path = self.default_folder + 'test_json'
        self.scheme_object = pickle.load(open(self.test_file_path + '.p', 'rb'))

    def test_machine_source_content(self):
        self.gen.make(self.scheme_object)

if __name__ == '__main__':
    unittest.main()

