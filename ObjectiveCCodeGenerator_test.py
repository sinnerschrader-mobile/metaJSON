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


class TestSampleTestStringOptionsCase(TestObjectiveCCodeGenerator):
    def setUp(self):
        super(TestSampleTestStringOptionsCase, self).setUp()
        self.test_file_path = self.default_folder + 'test_string_options'
        self.scheme_object = pickle.load(open(self.test_file_path + '.p', 'rb'))

    def test_machine_source_content(self):
        result = self.gen.machine_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MLoginJSONObject.m", result)

    def test_machine_header_content(self):
        result = self.gen.machine_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_S2MLoginJSONObject.h", result)

class TestSampleTestSubclassMotherCase(TestObjectiveCCodeGenerator):
    def setUp(self):
        super(TestSampleTestSubclassMotherCase, self).setUp()
        self.test_file_path = self.default_folder + 'test_subclass'
        self.scheme_object = pickle.load(open(self.default_folder + '/save_motherClass.p', 'rb'))

    def test_mother_human_header_content(self):
        result = self.gen.human_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/MotherClassJSONObject.h", result)

    def test_mother_human_source_content(self):
        result = self.gen.human_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/MotherClassJSONObject.m", result)

    def test_mother_machine_source_content(self):
        result = self.gen.machine_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_MotherClassJSONObject.m", result)

    def test_mother_machine_header_content(self):
        result = self.gen.machine_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_MotherClassJSONObject.h", result)

class TestSampleTestSubclassSubclassCase(TestObjectiveCCodeGenerator):
    def setUp(self):
        super(TestSampleTestSubclassSubclassCase, self).setUp()
        self.test_file_path = self.default_folder + 'test_subclass'
        self.scheme_object = pickle.load(open(self.default_folder + '/save_subClass.p', 'rb'))

    def test_subclass_human_header_content(self):
        result = self.gen.human_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/SubClassJSONObject.h", result)

    def test_subclass_human_source_content(self):
        result = self.gen.human_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/SubClassJSONObject.m", result)

    def test_subclass_machine_source_content(self):
        result = self.gen.machine_source_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_SubClassJSONObject.m", result)

    def test_subclass_machine_header_content(self):
        result = self.gen.machine_header_content(self.scheme_object)
        self.assert_content_file(self.test_file_path + "/_SubClassJSONObject.h", result)


if __name__ == '__main__':
    unittest.main()
