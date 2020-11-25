import unittest
from passwordmanager import Encryption

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.encryption = Encryption()
        self.key = self.encryption.generate_key()

    def test_ASCII(self):
        plain_text = 'fmZG18Cto'
        self.assertEqual(self.encryption.decrypt(self.encryption.encrypt(plain_text, self.key).decode(), self.key), plain_text)
        
        plain_text = ':oGb[ FlHX5#a^psr+2y'
        self.assertEqual(self.encryption.decrypt(self.encryption.encrypt(plain_text, self.key).decode(), self.key), plain_text)

    def test_unicode(self):
        plain_text = 'العربية'
        self.assertEqual(self.encryption.decrypt(self.encryption.encrypt(plain_text, self.key).decode(), self.key), plain_text)

        plain_text = '汉语'
        self.assertEqual(self.encryption.decrypt(self.encryption.encrypt(plain_text, self.key).decode(), self.key), plain_text)

        plain_text = '🦆🚀🔥🦕🧹🦈'
        self.assertEqual(self.encryption.decrypt(self.encryption.encrypt(plain_text, self.key).decode(), self.key), plain_text)


if __name__ == '__main__':
    unittest.main()