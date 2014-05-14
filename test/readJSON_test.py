import unittest
import os

class TestReadJSON(unittest.TestCase):
    def setUp(self):
        os.system("rm -rf ./src")

    def test_command(self):
        exit_status = self.execute_script("samples/product.json", "test/data/product")
        self.assertEqual(exit_status, 0) # no difference

    def execute_script(self, json_file, output_dir):
        os.system("python -m metajson -p '' -i " + json_file)
        # ignoring template files
        os.system("rm -rf ./src/Utilities")
        # return os.system("diff -r src/ " + output_dir)
        # common_file = "/AbstractInterfaceFiles/_ProductDetailJSONObject.h"
        # common_file = "/AbstractInterfaceFiles/_ProductDetailJSONObject.h"
        # common_file = "/AbstractInterfaceFiles/_SenderGroupJSONObject.h"
        # common_file = "/AbstractInterfaceFiles/_SenderList2JSONObject.h"
        # common_file = "/AbstractInterfaceFiles/_SenderListJSONObject.m"
        # common_file = "/AbstractInterfaceFiles/_SenderList2JSONObject.m"
        # common_file = "/AbstractInterfaceFiles/_SenderJSONObject.m"
        # common_file = "/AbstractInterfaceFiles/_SenderGroupJSONObject.m"
        return os.system("diff -r -w -b -B src " + output_dir)
        # return os.system("diff -r -w -b -B src" + common_file + " " + output_dir + common_file)

    def test_yaml_input(self):
        json_file = "samples/product.json"
        yaml_file = "samples/product.yaml"
        os.system("python -m metajson -i " + json_file + " -o src/json")
        os.system("python -m metajson -i " + yaml_file + " -o src/yaml")
        exit_status = os.system("diff -r -w -b -B src/json src/yaml")
        self.assertEqual(exit_status, 0) # no difference
