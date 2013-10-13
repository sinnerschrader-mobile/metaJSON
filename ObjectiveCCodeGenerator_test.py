from ObjectiveCCodeGenerator import *
from JSONScheme import *

import pickle
import unittest
import commands

class TestObjectiveCCodeGenerator(unittest.TestCase):
  def setUp(self):
    print('In setUp()')
    self.gen = ObjectiveCCodeGenerator()


  def tearDown(self):
    print('In tearDown()')
    del self.gen

  def test_getHeaderDescriptionString(self):
    result = self.gen.getHeaderDescriptionString("MyClass")
    expected_result = """//
//  MyClass.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

"""
    self.assertMultiLineEqual(result, expected_result)


  def test_getSourceDescriptionString(self):
    result = self.gen.getSourceDescriptionString("MyClass")
    expected_result = """//
//  MyClass.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

"""
    self.assertMultiLineEqual(result, expected_result)

  def test_makeMachineHeader(self):
    self.gen.dirPath = './src'
    schemeObject = pickle.load(open('test_data/schemeObj.p', 'rb'))
    self.gen.make(schemeObject)
    command = "diff src/AbstractInterfaceFiles/_S2MSenderJSONObject.h test_data/_S2MSenderJSONObject.h"
    status, output = commands.getstatusoutput(command)
    print output
    self.assertIs(status,0, "generated header file is different")

  def test_makeMachineSource(self):
    self.gen.dirPath = './src'
    schemeObject = pickle.load(open('test_data/schemeObj.p', 'rb'))
    self.gen.make(schemeObject)
    command = "diff src/AbstractInterfaceFiles/_S2MSenderJSONObject.m test_data/_S2MSenderJSONObject.m"
    status, output = commands.getstatusoutput(command)
    print output
    self.assertIs(status,0, "generated source file is different")

  def test_makeHumanHeader(self):
    self.gen.dirPath = './src'
    schemeObject = pickle.load(open('test_data/schemeObj.p', 'rb'))
    self.gen.make(schemeObject)
    command = "diff src/S2MSenderJSONObject.h test_data/S2MSenderJSONObject.h"
    status, output = commands.getstatusoutput(command)
    print output
    self.assertIs(status,0, "generated human header file is different")

  def test_makeHumanSource(self):
    self.gen.dirPath = './src'
    schemeObject = pickle.load(open('test_data/schemeObj.p', 'rb'))
    self.gen.make(schemeObject)
    command = "diff src/S2MSenderJSONObject.m test_data/S2MSenderJSONObject.m"
    status, output = commands.getstatusoutput(command)
    print output
    self.assertIs(status,0, "generated human source file is different")



if __name__ == '__main__':
    unittest.main()

