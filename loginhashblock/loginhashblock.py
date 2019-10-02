"""
LHB(login hash block) module is designed to work for account taker over attack - HMAC-based and PBKDF2 algorithms based.
It is compatible with python flask and application based on it

@version: 1.0.0
@authour: suwonchon(suwonchon@gmail.com)
@contact http://github.com/masuwonchon/loginblockchain
@license: MIT

Example usage:

"""

import random
import hashlib
import binascii

DEBUG = False


def print_LHBlist(LHBlistStr, DEBUG=False):
    """
    The function prints login hash block list for debug. 
    If login hash block list length is above 1, login hash block prints line by line.
    :param LHBlistStr:
    :return:
    """

    if LHBlistStr == None:
        text = '[info:print_LHBlist] user.Lhashblock:\n{}'.format(LHBlistStr)
        return True

    if len(LHBlistStr) < 1:
        text = '[info:print_LHBlist] user.Lhashblock:\n{}'.format(LHBlistStr)
        print(text)
    else:
        hblist = LHBlistStr.split(',')
        text = '[info:print_LHBlist] user.Lhashblock:'
        print(text)
        for i in hblist:
            print(i)

    return True

def pbkdf2_hash(data, salt, iterations, dklen=None, hash_name="sha256", DEBUG=False):
    """
    The function generated hash using PKCS#5 password-based key derivation function. 
    It uses HMAC as pseudorandom function and returns the hexadecimal representation of the binary data. 
    Every byte of data is converted into the corresponding 2-digit hex representation.
    :param data: data and salt are interpreted as buffers of byte
    :param salt: data and salt are interpreted as buffers of byte
    :param iterations: The number of iterations should be chosen based on the hash algorithm and computing power. 
                       As of 2013, at least 100,000 iterations of SHA-256 are suggested.
    :param dklen: dklen is the length of the derived key. 
                  If dklen is None then the digest size of the hash algorithm hash_name is used, e.g. 64 for SHA-512.
    :param hash_name: hash_name is the desired name of the hash digest algorithm for HMAC(default: sha256)
    :return:
    """

    if DEBUG:
        print('[info:pdkdf2_ascii] hash: ', hash_name)
        print('[info:pdkdf2_ascii] iterations: ', iterations)
        print('[info:pdkdf2_ascii] data: ', data.encode('ascii'))
        print('[info:pdkdf2_ascii] salt: ', salt.encode('ascii'))

    dk = hashlib.pbkdf2_hmac(hash_name, data.encode('ascii'), salt.encode('ascii'), iterations, dklen=dklen)
    hex = binascii.hexlify(dk)
    return hex.decode('ascii')

def create_salt(length, RAND_CHARS=None, DEBUG=False):
    """
    This function generate a random string of SALT_CHARS with specified length.
    :param length: salt length
    :param RAND_CHARS: random chars
    :return:
    """
    if not RAND_CHARS:
        RAND_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#%^&*()"

    randx = list()
    for x in range(length):
         randx.append(random.choice(RAND_CHARS))

    salt = ''.join(randx)
    return salt

def create_loginhashblocklist(LHBlistStr, DEBUG=DEBUG):
    """
    This function create login hash block list. First of all it generate device id and then it makes login hash block string. 
    Finally it update the login hash block list that was joined with login hash block.
    :param LHBlistStr: previous login hash block list
    :return:
    """

    devid = create_deviceId(DEBUG=DEBUG)
    LHBstr = create_loginhashblock(devid, DEBUG=DEBUG)
    uLHBlistStr, uLHBstr = update_loginhashblocklist(LHBlistStr, LHBstr)

    return uLHBlistStr, uLHBstr

def update_loginhashblocklist(LHBlistStr, prevLHBstr, DEBUG=False):
    """
    This function update login hash block list. 
    It's parsed device id from input login hash block and then it will be updat to new hash block binded parsed device id. 
    If LHBlistStr is null, LHBlistStr will be prevLHBstr. 
    And, the other case is updating login hash block from the list.
    :param LHBlistStr: login hash block list string
    :param LHBstr: login hash block
    :return:
    """

    LHBstr = update_loginhashblock(prevLHBstr, DEBUG=False)

    if not LHBstr:
        return LHBlistStr, LHBstr

    devid = get_deviceId(LHBstr, DEBUG=DEBUG)

    if not LHBlistStr:
        LHBlistStr = LHBstr
        
        if DEBUG:
            print("[info:update_loginhashblocklist] LHBlistStr is null")

        return LHBlistStr, LHBstr

    LHBlist = LHBlistStr.split(',')

    for i,v in enumerate(LHBlist):
        _devid = get_deviceId(v, DEBUG=DEBUG)
        if devid == _devid:
            LHBlist[i] = LHBstr
            LHBlistStr = ",".join(LHBlist)
            return LHBlistStr, LHBstr

    LHBlist.append(LHBstr)

    if DEBUG:
        print("[info:update_loginhashblocklist] devid: {}".format(devid))
        print("[info:update_loginhashblocklist] db_hashblock: {}".format(len(LHBlist)))

    LHBlistStr = ",".join(LHBlist)

    return LHBlistStr, LHBstr

def create_hash(salt, target, hash_name="sha256", iterations=100000, kdf=None, DEBUG=False):
    """
    This function is to obtain the digest of the byte target string, It uses HMAC as pseudorandom function.
    :param salt, target: Target and salt are interpreted as buffers of bytes.
    :param hash_name: The string hash_name is the desired name of the hash digest algorithm for HMAC
    :param iterations: The number of iterations should be chosen based on the hash algorithm and computing power. 
    :param kdf: key derivation function(ex, bcrypt, PBKDF2 etc)
    :return:
    """

    if not target or not salt:
        raise ValueError("[info:create_hash] target string or salt is null")

    if not kdf:
        h = hashlib.new(hash_name)
        h.update(target.encode('ascii'))
        hash = h.hexdigest()
        method = "none:%s:%d" % (hash_name, iterations)
    else:
        if kdf == "pbkdf2":
            hash = pbkdf2_hash(target, salt, iterations, hash_name=hash_name)
            method = "pbkdf2:%s:%d" % (hash_name, iterations)
        elif kdf == "scrypt":
            raise ValueError("[info:create_hash] will be supported")
        else:
            raise ValueError("[info:create_hash] Invalid support key derivation function")

    if DEBUG:
        text = "[info:create_hash] hash: {}, method: {}".format(hash, method)
        print(text)

    return hash, method

def valid_hash(target_hash, salt, target, method, DEBUG=False):
    """
    This function is to check hash block
    :param target_hash:
    :param salt:
    :param target:
    :param method:
    :return:
    """

    if method.count(":") != 2:
        return False

    kdf, hash_name, iterations = method.split(":", 2)
    hash, method = create_hash(salt, target, hash_name=hash_name, iterations=int(iterations), kdf=kdf)
    ret = compare_loginhashblock(hash, target_hash)

    if DEBUG:
        print("[info:valid_hash]        hash: ", hash)
        print("[info:valid_hash] target_hash: ", target_hash)
        print("[info:valid_hash]         ret: ", ret)

    return ret

def get_deviceId(LHBstr, DEBUG=False):
    """
    This function is to get device id from login hash block. 
    Login hash block is on device id and hashblock divided by special characters '$'.
    :param LHBstr: string of login hash block
    :return:
    """

    if DEBUG:
        print("[info:get_deviceId] LHBstr: {}".format(LHBstr))

    if not LHBstr:
        raise ValueError("[info:get_deviceId] login hash block is null")

    if not valid_loginhashblock(LHBstr, DEBUG=DEBUG):
        raise ValueError("[info:get_deviceId] Invalid login hash block")

    devid, loginhash = LHBstr.split("$", 1)
    return devid

def create_deviceId(DEBUG=False):
    """
    This function is to generate device id, Device id is used to identify client computer, terminal and environment. 
    DeviceId is created by random string as a magic number
    :return:
    """

    RAND_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    devid = create_salt(8, RAND_CHARS=RAND_CHARS)

    if DEBUG:
        text = "[info:create_deviceId] devid: {}".format(devid)
        print(text)

    return devid

def compare_loginhashblock(a, b, DEBUG=False):
    """
    This function is to compare tow login hash block. If these are same, it return True. others cases, it return False
    :param a: compare login hash block
    :param b: compare login hash block
    :return: Bool
    """

    if DEBUG:
        print("[info:compare_loginhashblock] a: ",a)
        print("[info:compare_loginhashblock] b: ",b)

    if isinstance(a, str):
        a = a.encode("utf-8")

    if isinstance(b, str):
        b = b.encode("utf-8")

    if len(a) != len(b):
        return False

    for x, y in zip(a, b):
        if x != y:
            return False

    return True

def verify_loginhashblock(LHBlistStr, LHBstr, DEBUG=False):
    """
    This function verify login hash block in db or not. 
    It parse the device id from input login hash block, and search device id in login hash block list string. 
    If it matched, return True
    :param LHBlistStr: login hash block list
    :param LHBstr: login hash block
    :return:
    """

    if not LHBlistStr :
        return False

    devid = get_deviceId(LHBstr, DEBUG=DEBUG)
    LHBlist = LHBlistStr.split(',')

    for i,v in enumerate(LHBlist):
        _devid = get_deviceId(v, DEBUG=DEBUG)
        if devid == _devid:
            if v == LHBstr:
                return True
            else:
                return False

    return False

def valid_loginhashblock(LHBstr, DEBUG=False):
    """
    This function is to check login hash block
    hashblock format: deviceid(8)+$+hash
    ex) jUs6LQMX$jUs6LQMX$ceccffbfa52e55825f87573b068c8d759b1540f9833a7d7ebd7a27c993ffd316
    :param LHBstr:
    :return: BOOL
    """
    if not LHBstr:
        if DEBUG:
            print('[info:valid_loginhashblock] Null')
        return False

    if LHBstr.count("$") != 1:
        if DEBUG:
            print('[info:valid_loginhashblock] Invalid format')
        return False

    devid, hash = LHBstr.split("$", 1)

    if len(devid) != 8:
        if DEBUG:
            print('[info:valid_loginhashblock] Invalid deviceid')
        return False

    if len(hash) != 64:
        return False

    if DEBUG:
        print('[info:valid_loginhashblock] login hash block is valid')

    return True

def update_loginhashblock(prevLHBstr, DEBUG=False):
    """
    This function update login hash block with previous login hash block.
    :param prevLHBstr:
    :param DEBUG:
    :return: updated login hash block
    """

    if not prevLHBstr:
        return None

    if not valid_loginhashblock(prevLHBstr, DEBUG=DEBUG):
        raise ValueError("[info:update_loginhashblock] Invalid login hash block")

    devid = get_deviceId(prevLHBstr, DEBUG=DEBUG)
    LHBstr = create_loginhashblock(devid, DEBUG=DEBUG)

    if DEBUG:
        text = '[info:update_loginhashblock] \npre_loginhashblock: {}\nnew_loginhashblock: {}'.format(prevLHBstr,LHBstr)
        print(text)

    return LHBstr

def isRegistedLHB(LHBstr, LHBlistStr, DEBUG=False):
    """
    This function is to check valid previous login hash block.
    :LHBstr: client's login hash block
    :LHBlistStr: client's login has block in database
    """

    LHBlist = LHBlistStr.split(',')

    if not valid_loginhashblock(LHBstr, DEBUG=DEBUG):
        return False

    devid = get_deviceId(LHBstr, DEBUG=DEBUG)
    target_LHBstr = get_loginhashblock(devid, LHBlist, DEBUG=DEBUG)

    if DEBUG:
        print("[info:isRegistedLHB]\nclient_loginhashblock: {}\nserver_loginhashblock: {}".format(LHBstr, target_LHBstr))

    if LHBstr == target_LHBstr:
        return True

    return False

def get_loginhashblock(devid, LHBlist, DEBUG=False):
    """
    This function is to get login hash block by device id in login hash block list.
    :devid: device id
    :LHBlist: client's login has block in database
    :return:
    """

    for LHBstr in LHBlist:
        _devid = get_deviceId(LHBstr, DEBUG=DEBUG)
        if devid == _devid:
            if DEBUG:
                print('[info:get_loginhashblock] devid is found in login hash block list')
            return LHBstr

    if DEBUG:
        print('[info:get_loginhashblock] devid is not found in login hash block list')

    return ''

def create_loginhashblock(devid, key=None, DEBUG=False):
    """
    This functions is to generate login hash block with device id.
    :param devid:
    :param key:
    :return: login hash block
    """

    if not devid:
        raise ValueError("[info:create_loginhashblock] devid is null")

    if not key:
        key = 'HKAHJFKIIJF'

    length = 8
    kdf = 'pbkdf2'
    salt = create_salt(length)
    hash, method = create_hash(salt, key, kdf=kdf)

    if DEBUG:
        text = "[info:create_loginhashblock] salt: {}, method: {}, hash: {}, devid: {}".format(salt, method, hash, devid)
        print(text)

    LHBstr = '{}${}'.format(devid, hash)

    return LHBstr
