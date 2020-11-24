import unittest
from passwordmanager import Encryption

class TestStringMethods(unittest.TestCase):
    
    def test_numbers(self):
        self.assertEqual('meme', 'meme')

if __name__ == '__main__':
    unittest.main()