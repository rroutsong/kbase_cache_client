from kbase_cache_client.kbase_cache_client import KBaseCacheClient
import unittest
import os
import shutil


class TestKbaseCacheClient(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.KBC = KBaseCacheClient('https://appdev.kbase.us/services/')
        cls.test_dir = os.path.join(os.path.dirname(__file__), 'tests')
        if not os.path.exists(cls.test_dir):
            os.mkdir(cls.test_dir)
        cls.test_file = os.path.join(cls.test_dir, 'tests.txt')
        if not os.path.exists(cls.test_file):
            text_file = open(cls.test_file, "w")
            text_file.write('This is the file to test the cache client module')
            text_file.close()
            
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

    def test_gen_cache_id(self):
        cacheid = self.KBC.generate_cacheid({'test': 'this is a test identifier to id a cache file'})
        print(f'Cache ID is {cacheid}')
        self.KBC.upload_cache(cacheid, self.test_file)
        print('Cache uploaded.')
        destinationdir = os.path.join(self.test_dir, 'cache')
        os.mkdir(destinationdir)
        destination = os.path.join(destinationdir, 'cachedl.txt')
        self.KBC.download_cache(cacheid, destination)
        print('Cache downloaded.')
        self.KBC.delete_cache(cacheid)
        print('Cache deleted.')

if __name__ == '__main__':
    unittest.main()
