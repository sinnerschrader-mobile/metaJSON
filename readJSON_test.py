import unittest
import os

class TestReadJSON(unittest.TestCase):
    def setUp(self):
        os.system("rm -rf src")

    def test_command(self):
        exit_status = self.execute_script("samples/product.json", "test_data/product")
        self.assertEqual(exit_status, 0) # no difference

    def execute_script(self, json_file, output_dir):
        os.system("python readJSON.py -i " + json_file)
        # ignoring template files
        os.system("rm -rf src/Utilities")
        # return os.system("diff -r src/ " + output_dir)
        # common_file = "/AbstractInterfaceFiles/_ProductDetailJSONObject.h"
        common_file = "/AbstractInterfaceFiles/_SenderGroupJSONObject.h"
        return os.system("diff -r -B src" + common_file + " " + output_dir + common_file)