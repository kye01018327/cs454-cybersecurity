from aes import *
from utils import *

def test_aes_decryption():
    textbook_plaintext = 0x0123456789abcdeffedcba9876543210
    textbook_key = 0x0f1571c947d9e8590cb7add6af7f6798
    textbook_ciphertext = 0xff0b844a0853bf7c6934ab4364148fb9
    ciphertext = aes_encrypt(textbook_plaintext, textbook_key)
    plaintext = aes_decrypt(ciphertext, textbook_key)
    assert plaintext == textbook_plaintext