from __future__ import absolute_import, division, unicode_literals
from Crypto.Cipher import AES
import pymongo
import urllib.parse
username = urllib.parse.quote_plus('rkms')
password = urllib.parse.quote_plus('2Password!')
mongouri = f'mongodb://{username}:{password}@192.168.100.193:27017/?authMechanism=SCRAM-SHA-1&authSource=RKMS_DB'
dbname = 'RKMS_DB'
myclient = pymongo.MongoClient(mongouri)
mydb = myclient[dbname]

class AES_test:
    def __init__(self,hex_key,iv):
        
        self.key = bytes.fromhex(hex_key)
        self._IV = bytes.fromhex(iv)

    def aes_encrypt(self,data):
        cryptor = AES.new(self.key, AES.MODE_CBC, self._IV)
        data = self.__pad(data)
        return cryptor.encrypt(data)

    def aes_decrypt(self,data):
        cryptor = AES.new(self.key, AES.MODE_CBC, self._IV)
        data = bytes.fromhex(data)
        a=self.__unpad(cryptor.decrypt(data)).decode('utf-8')
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
    hex_string ="0aac999f50088c8f59cde5781c787ae6"
    #data=bytes.fromhex(hex_string)
    ## print(type(data))

    hex_key="D66A048AF9066E68C78BE48D6800267D88B2CD2049E442C5E743E5D2465513CC"
    #key=bytes.fromhex(hex_key)
    # dec = AES_test(data,key).aes_decrypt

    prpcrpto= AES_test(hex_string,hex_key)
    print(prpcrpto.aes_decrypt())
    #DEC=dec.decode('utf-8')
    #print(DEC)