import datetime
import difflib
import os
import re
import shutil
import sys
import unittest

class TestReadJSON(unittest.TestCase):
    def setUp(self):
        os.system("rm -rf ./src")

    def test_command(self):
        exit_status = self.execute_script("samples/product.json", "test/data/product")
        self.assertTrue(exit_status)

    def execute_script(self, json_file, output_dir):
        os.system("python -m metajson -p '' -i " + json_file)
        # ignoring template files
        shutil.rmtree(os.path.join("src", "APIParser"))
        shutil.rmtree(os.path.join("src", "Utilities"))
        return self.compare_dirs("src", output_dir, fix_date = True)

    def test_yaml_input(self):
        json_file = os.path.join("samples", "product.json")
        yaml_file = os.path.join("samples", "product.yaml")
        json_out_dir = os.path.join("src", "json")
        yaml_out_dir = os.path.join("src", "yaml")
        os.system("python -m metajson -i " + json_file + " -o " + json_out_dir)
        os.system("python -m metajson -i " + yaml_file + " -o " + yaml_out_dir)
        exit_status = self.compare_dirs(json_out_dir, yaml_out_dir)
        self.assertTrue(exit_status)

    def compare_dirs(self, dir_a, dir_b, fix_date = False):
        files_in_a = []
        for (dirpath, subdirs, filenames) in os.walk(dir_a):
            current_dir = dirpath
            for filename in filenames:
                cur_file_path_a = os.path.join(dirpath,filename)
                cur_file_path_b = cur_file_path_a.replace(dir_a, dir_b, 1)
                if not os.path.isfile(cur_file_path_b):
                    print "%s not found in %s." % (current_file_path_a, dir_b)
                    return False
                files_in_a += [cur_file_path_a]
                content_a = "foo"
                content_b = "bar"
                cur_file_a = open(cur_file_path_a, 'r')
                cur_file_b = open(cur_file_path_b, 'r')
                try: 
                    content_a = cur_file_a.read()
                    if fix_date:
                        # All timestamps in reference files should be 2014, so we need to tweak our generated files to match them.
                        content_a = content_a.replace(str(datetime.datetime.now().year), "2014")
                    content_a = re.sub("\s", "", content_a)
                    content_b = re.sub("\s", "", cur_file_b.read())
                finally:
                    cur_file_a.close()
                    cur_file_b.close()
                if content_a != content_b:
                    for line in difflib.unified_diff(content_a, content_b, fromfile=cur_file_path_a, tofile=cur_file_path_b):
                        sys.stdout.write(line)
                    return False
        for (dirpath, subdirs, filenames) in os.walk(dir_b):
            for filename in filenames:
                current_file_name = os.path.join(dirpath, filename)
                if not (current_file_name.replace(dir_b, dir_a, 1) in files_in_a):
                  print "%s not found in %s" % (current_file_name, dir_a)
                  return False
        return True

