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
    def __init__(self,hex_string,hex_key,iv):
        self.data = bytes.fromhex(hex_string)
        self.key = bytes.fromhex(hex_key)
        self._IV = bytes.fromhex(iv)

    def aes_encrypt(self):
        cryptor = AES.new(self.key, AES.MODE_CBC, self._IV)
        return cryptor.encrypt(self.data)

    def aes_decrypt(self):
        unpad = lambda s : s[0:s[-1]]
        cryptor = AES.new(self.key, AES.MODE_CBC, self._IV)
        a=unpad(cryptor.decrypt(self.data)).decode('utf-8').strip('\x01')
        return a

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