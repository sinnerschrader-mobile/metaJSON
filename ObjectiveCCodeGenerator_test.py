from ObjectiveCCodeGenerator import *
from JSONScheme import *

import pickle
import unittest
import commands

class TestObjectiveCCodeGenerator(unittest.TestCase):
  def setUp(self):
    self.gen = ObjectiveCCodeGenerator()
    self.gen.dirPath = './src'
    self.maxDiff = None
    default_folder = 'test_data/'
    self.test_file_path = default_folder + 'test_class'

    self.scheme_sender_object = pickle.load(open(self.test_file_path + '.p', 'rb'))

  def tearDown(self):
    del self.gen

  def test_human_header_content(self):
    result = self.gen.human_header_content(self.scheme_sender_object)
    self.assert_content_file(self.test_file_path + "/S2MSenderJSONObject.h", result)

  def test_human_source_content(self):
    result = self.gen.human_source_content(self.scheme_sender_object)
    self.assert_content_file(self.test_file_path + "/S2MSenderJSONObject.m", result)

  def test_machine_source_content(self):
    result = self.gen.machine_source_content(self.scheme_sender_object)
    self.assert_content_file(self.test_file_path + "/_S2MSenderJSONObject.m", result)

  def test_machine_header_content(self):
    result = self.gen.machine_header_content(self.scheme_sender_object)
    self.assert_content_file(self.test_file_path + "/_S2MSenderJSONObject.h", result)

  def assert_content_file(self, filename, content):
    with open(filename, 'r') as content_file:
        expected_result = content_file.read()
    self.assertMultiLineEqual(content, expected_result)

if __name__ == '__main__':
    unittest.main()

