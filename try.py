from __future__ import absolute_import, division, unicode_literals
from Crypto.Cipher import AES
import logging


class AES_test:
    def __init__(self,hex_key):
        self.key = bytes.fromhex(hex_key)
        self._IV = 16 * '\x00'

    def aes_encrypt(self,data):
        raw = self.__pad(data)
        cipher = AES.new(self.key, AES.MODE_CBC,self._IV)
        return (cipher.encrypt(raw)).hex()

    def aes_decrypt(self,data):
        cryptor = AES.new(self.key, AES.MODE_CBC, self._IV)
        data = bytes.fromhex(data)
        a=self.__unpad(cryptor.decrypt(data)).hex()
        return a

    def __unpad(self,text):
        # print(type(text))
        pad = text[-1]
        return text[:-pad]
        
    def __pad(self, text):
        text = bytes.fromhex(text)
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        # pad = bytes.fromhex(hex(amount_to_pad)[2:])
        pad = bytearray([amount_to_pad])
        for x in range(amount_to_pad):
            text = text + pad
        return text

if __name__=="__main__":
    ##convert hexstring to byte
    # hex_string ="0aac999f50088c8f59cde5781c787ae6"
    hex_key="D66A048AF9066E68C78BE48D6800267D88B2CD2049E442C5E743E5D2465513CC"
    enc = AES_test(hex_key)
    data ="0123456789abcdefabcdef0123456789"
    c=enc.aes_encrypt(data)
    print("C:")
    print(c)
    dec = AES_test(hex_key)
    d = dec.aes_decrypt(c)
    print("D:")
    print(d)


