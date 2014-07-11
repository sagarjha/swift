from Crypto.Cipher import AES
#base64 is used for encoding. dont confuse encoding with encryption#
#encryption is used for disguising data
#encoding is used for putting data in a specific format
import base64
# os is for urandom, which is an accepted producer of randomness that
# is suitable for cryptology.
import os
from itertools import izip, cycle


key = '\xb9\x1d\xb5\xb9\xc3\xad\xdb\xb3?\xc0\xd7M\x8c\x8c\xe8e'

#32 bytes = 256 bits
#16 = 128 bits
# the block size for cipher obj, can be 16 24 or 32. 16 matches 128 bit.
BLOCK_SIZE = 16

def AES_encryption(privateInfo, key):

    
    # the character used for padding
    # used to ensure that your value is always a multiple of BLOCK_SIZE
    PADDING = '{'
    
    # function to pad the functions. Lambda
    # is used for abstraction of functions.
    # basically, its a function, and you define it, followed by the param
    # followed by a colon,
    # ex = lambda x: x+5
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    
    # encrypt with AES, encode with base64
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    
    # creates the cipher obj using the key
    cipher = AES.new(key)
    
    # encodes you private info!
    encoded = EncodeAES(cipher, privateInfo)

    # print 'Encrypted string:', encoded
    return encoded

def DES_decryption(encryptedString, key):

    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    #Key is FROM the printout of 'secret' in encryption
    #below is the encryption.
    encryption = encryptedString
    cipher = AES.new(key)
    decoded = DecodeAES(cipher, encryption)
    return decoded

def xor_crypt_string(data, key):
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
