from Crypto import Random
from Crypto.Cipher import AES
import os 
import os.path
from os import listdir
from os.path import isfile
from os import walk
import time

class Encryptor : 
    def __init__(self , key) : 
        self.key=key
    
    def pad(self , s) :
        return s+b"\0" * (AES.block_size - len(s) % AES.block_size)
    
    def encrypt(self , message , key , key_size = 256 ) :
        message =  self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key , AES.MODE_CBC , iv)
        return iv + cipher.encrypt(message)
    
    def encrypt_file(self , file_name):
        if(file_name[-4:] != ".enc"):
            with open(file_name,'rb') as fo:
                plaintext = fo.read()
            enc = self.encrypt(plaintext , self.key)
            with open(file_name + ".enc" , 'wb') as fo:
                fo.write(enc)
            os.remove(file_name)
        else:
            print("  File already encrypted    ")

    def decrpt(self , cipherText , key):
        iv = cipherText[:AES.block_size]
        cipher = AES.new(key , AES.MODE_CBC , iv)
        plaintext = cipher.decrypt(cipherText[AES.block_size:])
        return plaintext.rstrip(b"\0")
    
    def decrypt_file(self , file_name):
        if(file_name[-4:] == ".enc"):
            with open(file_name , 'rb') as fo:
                cipherText = fo.read()
            dec = self.decrpt(cipherText , self.key)
            with open(file_name[:-4] , 'wb') as fo:
                fo.write(dec)
            os.remove(file_name)
        else:
            print("  File already decrypted    ")
    
    def getAllFiles(self , path):
        filepaths = []
        for (dirpath , dirname , filename) in walk(path):
            for f in filename:
                filepaths.append(dirpath + "\\" + f)
        return filepaths

    def encrypt_all_files(self , path):
        dirs = self.getAllFiles(path)
        for file_path in dirs:
            self.encrypt_file(file_path)
    
    def decrypt_all_files(self , path):
        dirs = self.getAllFiles(path)
        for file_path in dirs:
            self.decrypt_file(file_path)

key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)
clear = lambda: os.system('cls')


while(True) : 
    s = str(input("\nEnter file or folder path : "))
    while(os.path.isfile(s)==False and os.path.isdir(s)==False):
        print("\nInvalid file or folder path")
        clear()
        s = str(input("\nEnter file or folder path : "))

    do = str(input("\ne: encryption \nd: decryption \nEnter e/d: "))
    while(do!="e" and do!="d"):
        print("\nInvalid input")
        clear()
        do = str(input("\ne: encryption \n d: decryption \nEnter e/d"))

    #print("Wait while task gets completed")

    if (os.path.isfile(s)==True and do=="e") :
        enc.encrypt_file(s)
    elif (os.path.isdir(s)==True and do=="e") :
        enc.encrypt_all_files(s)
    elif (os.path.isfile(s)==True and do=="d") :
        enc.decrypt_file(s)
    elif (os.path.isdir(s)==True and do=="d") :
        enc.decrypt_all_files(s)
    
    #time.sleep(15)
    
