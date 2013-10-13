from ObjectiveCCodeGenerator import *


import unittest

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

if __name__ == '__main__':
		unittest.main()

