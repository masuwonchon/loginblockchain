"""
Unittest for LHB(login hash block) module

@version: 1.0.0
@authour: suwonchon(suwonchon@gmail.com)
@contact http://github.com/masuwonchon
@license: MIT

Example usage:
"""

from loginhashblock import *

def unittest_get_loginhashblock():
    print("[Unittest:get_loginhashblock] RUN")
    get_loginhashblock(DEBUG=True)
    return True

def unittest_update_loginhashblock():
    print("[Unittest:update_loginhashblock] RUN")
    loginhashblock = 'aCIXQRZR$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a0'
    update_loginhashblock(loginhashblock, DEBUG=True)

    loginhashblock = 'aCIXQRZ$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a0'
    return True

def unittest_replace_hashblock():
    list_loginhashblock = "1CIXQRZR$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1,2CIXQRZR$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2,3CIXQRZR$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a3,4CIXQRZR$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a4"
    #list_loginhashblock = "1CIXQRZR$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1"
    #list_loginhashblock = ""
    loginhashblock = '1CIXQRZR$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a5'
    data = update_loginhashblocklist(list_loginhashblock, loginhashblock, DEBUG=True)
#    data = ",".join(lhblist)
    print(data)

def unittest_pbkdf2_ascii():
    TargetStr = 'password'
    iterations = 100000
    hash = ['ripemd160', 'sha256', 'sha512']

    for i in hash:
        salt = create_salt(8)
        dk = pbkdf2_hash(TargetStr, salt, iterations, hash_name=i)
        print('TargetStr: ', TargetStr)
        print('ret0: ', dk)

    return True

unittest_pbkdf2_ascii()
unittest_replace_hashblock()
