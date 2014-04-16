import unittest

import datetime
import time
import os
import sys
from pystache import Renderer

# run nosetests -s mustache_test.py
class TestMustache(unittest.TestCase):

    def assert_content_file(self, filename, content):
        with open(filename, 'r') as content_file:
            expected_result = content_file.read()
        self.assertMultiLineEqual(content, expected_result)

    def test_mustache_machine_m(self):
      templateFile = open(self.template_file_path("machine.m.mustache"), "r")
      today = datetime.date.fromtimestamp(time.time())

      idProp = {'varName': 's2mId', 'name': 'id'}
      firstName = {'varName': 'firstName', 'name': 'firstName'}
      myNumber = {'varName': 'myNumber', 'name': 'myNumber'}

      stringProperties = [idProp, firstName]
      numberProperties = [myNumber]
      hashParams = {"date": str(today.year), "machineClassName": "_MyObject", "projectPrefix": "S2M", "humanClassName": "MyObject", "variableName": "myObject", "stringProperties": stringProperties, 'numberProperties': numberProperties}

      result = Renderer().render(templateFile.read(), hashParams)
      print result
      # self.assert_content_file(self.test_file_path + "/_S2MSenderJSONObject.h", result)

    def template_file_path(self, filename) :
        templatePath = os.path.realpath( __file__ )
        templatePath = templatePath.replace(os.path.basename( __file__ ), 'templates')
        return os.path.join(templatePath, filename)


if __name__ == '__main__':
    unittest.main()
