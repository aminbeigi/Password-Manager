import unittest
from passwordmanager import Encryption

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.encryption = Encryption()
        self.key = self.encryption.generate_key()

    def test_numbers(self):
        plain_text = 'fmZG18Cto'
        self.assertEqual(self.encryption.decrypt(self.encryption.encrypt(plain_text, self.key).decode(), self.key), plain_text)

if __name__ == '__main__':
    unittest.main()