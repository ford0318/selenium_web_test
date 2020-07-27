from __future__ import absolute_import, division, unicode_literals
from Crypto.Cipher import AES

class AES_test:
    def __init__(self,hex_string,hex_key):
        self.data = bytes.fromhex(hex_string)
        self.key = bytes.fromhex(hex_key)
        self._IV = 16 * '\x00'

    def aes_encrypt(self):
        cryptor = AES.new(self.key, AES.MODE_CBC, self._IV)
        return cryptor.encrypt(self.data)

    def aes_decrypt(self):
        cryptor = AES.new(self.key, AES.MODE_CBC, self._IV)
        a=cryptor.decrypt(self.data).decode('utf-8')
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