from kbase_cache_client.kbase_cache_client import KBaseCacheClient
import unittest
import os
import shutil


class TestKbaseCacheClient(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.KBC = KBaseCacheClient('https://ci.kbase.us/services/')
        cls.test_dir = os.path.join(os.path.basename(__file__), 'tests')
        cls.test_file = os.path.join(cls.test_dir, 'tests.txt')

        text_file = open(cls.test_file, "w")
        text_file.write('This is the file to test the cache client module')
        text_file.close()

    @classmethod
    def tearDownClass(cls):
        shutils.rmtree(cls.test_dir)

    def test_gen_cache_id(self):
        return True

    def test_upload_cache(self):
        return True

    def test_download_cache(self):
        return True

    def test_delete_cache(self):
        return True


if __name__ == '__main__':
    unittest.main()
