from ObjectiveCCodeGenerator import *
from JSONScheme import *

import pickle
import unittest
import commands

class TestObjectiveCCodeGenerator(unittest.TestCase):
  def setUp(self):
    print('In setUp()')
    self.gen = ObjectiveCCodeGenerator()
    self.gen.dirPath = './src'
    self.maxDiff = None

  def tearDown(self):
    print('In tearDown()')
    del self.gen

  def test_makeMachineHeader(self):
    schemeObject = pickle.load(open('test_data/schemeObj.p', 'rb'))
    self.gen.make(schemeObject)
    command = "diff src/AbstractInterfaceFiles/_S2MSenderJSONObject.h test_data/_S2MSenderJSONObject.h"
    status, output = commands.getstatusoutput(command)
    print output
    self.assertIs(status,0, "generated header file is different")

  def test_makeMachineSource(self):
    schemeObject = pickle.load(open('test_data/schemeObj.p', 'rb'))
    self.gen.make(schemeObject)
    command = "diff src/AbstractInterfaceFiles/_S2MSenderJSONObject.m test_data/_S2MSenderJSONObject.m"
    status, output = commands.getstatusoutput(command)
    print output
    self.assertIs(status,0, "generated source file is different")

  def test_makeHumanHeader(self):
    schemeObject = pickle.load(open('test_data/schemeObj.p', 'rb'))
    self.gen.make(schemeObject)
    command = "diff src/S2MSenderJSONObject.h test_data/S2MSenderJSONObject.h"
    status, output = commands.getstatusoutput(command)
    print output
    self.assertIs(status,0, "generated human header file is different")

  def test_makeHumanSource(self):
    schemeObject = pickle.load(open('test_data/schemeObj.p', 'rb'))
    self.gen.make(schemeObject)
    command = "diff src/S2MSenderJSONObject.m test_data/S2MSenderJSONObject.m"
    status, output = commands.getstatusoutput(command)
    print output
    self.assertIs(status,0, "generated human source file is different")

  def test_machine_header_content(self):
    schemeObject = pickle.load(open('test_data/schemeObj.p', 'rb'))
    with open("test_data/_S2MSenderJSONObject.h", 'r') as content_file:
        expected_result = content_file.read()
    result = self.gen.machine_header_content(schemeObject)
    self.assertMultiLineEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()

