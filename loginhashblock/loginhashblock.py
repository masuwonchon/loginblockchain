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


def print_LHBlist(LHBliststr, DEBUG=False):
    """
    The function prints login hash block list for debug.
    :param LHBliststr:
    :return:
    """

    if LHBliststr == None:
        text = '[info:print_LHBlist] user.Lhashblock:\n{}'.format(LHBliststr)
        return True

    if len(LHBliststr) < 1:
        text = '[info:print_LHBlist] user.Lhashblock:\n{}'.format(LHBliststr)
        print(text)
    else:
        hblist = LHBliststr.split(',')
        text = '[info:print_LHBlist] user.Lhashblock:'
        print(text)
        for i in hblist:
            print(i)

    return True

def pbkdf2_hash(data, salt, iterations, dklen=None, hash_name="sha256", DEBUG=False):
    """
    The function provides PKCS#5 password-based key derivation function.
    It uses HMAC as pseudorandom function.
    eturn the hexadecimal representation of the binary data. Every byte of data is converted into the corresponding 2-digit hex representation.
    :param data: data and salt are interpreted as buffers of byte
    :param salt: data and salt are interpreted as buffers of byte
    :param iterations: The number of iterations should be chosen based on the hash algorithm and computing power. As of 2013, at least 100,000 iterations of SHA-256 are suggested.
    :param dklen: dklen is the length of the derived key. If dklen is None then the digest size of the hash algorithm hash_name is used, e.g. 64 for SHA-512.
    :param hash_name: hash_name is the desired name of the hash digest algorithm for HMAC(default: sha256)
    :param DEBUG: debug option flags
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

def update_loginhashblocklist(loginhashblocklist, loginhashblock, DEBUG=False):
    """
    This function replace login hash block in data bases.
    :param list: login hash block list
    :param loginhashblock: login hash block
    :return:
    """

    devid = get_deviceId(loginhashblock, DEBUG=DEBUG)

    if not loginhashblocklist :
        return loginhashblock

    loginhashblocklist = loginhashblocklist.split(',')

    if len(loginhashblocklist) < 8:
        return loginhashblock

    if DEBUG:
        print("[info:update_loginhashblocklist] devid: {}, hash: {}".format(devid, hash))
        print("[info:update_loginhashblocklist] db_hashblock: {}".format(len(loginhashblocklist)))

    for i,v in enumerate(loginhashblocklist):
        get_devid = get_deviceId(v, DEBUG=DEBUG)
        if devid == get_devid:
            loginhashblocklist[i] = loginhashblock
            return ",".join(loginhashblocklist)

    loginhashblocklist.append(loginhashblock)
    return ",".join(loginhashblocklist)

def create_hash(salt, target, hash_name="sha256", iterations=100000, kdf=None, DEBUG=False):
    """
    This function is to obtain the digest of the byte target string, It uses HMAC as pseudorandom function.
    :param salt, target: Target and salt are interpreted as buffers of bytes.
    :param hash_name: The string hash_name is the desired name of the hash digest algorithm for HMAC
    :param iterations: The number of iterations should be chosen based on the hash algorithm and computing power. As of 2013, at least 100,000 iterations of SHA-256 are suggested.
    :param kdf: key derivation function(ex, bcrypt, PBKDF2 etc)
    :return: hash, method
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

def get_deviceId(loginhashblock, DEBUG=False):
    """
    This function is to get device id from login hash block
    :param hashblock:
    :param DEBUG:
    :return:
    """

    if DEBUG:
        print("[info:get_deviceId] loginhashblock: {}".format(loginhashblock))

    if not loginhashblock:
        raise ValueError("[info:get_deviceId] login hash block is null")

    if not valid_loginhashblock(loginhashblock, DEBUG=DEBUG):
        raise ValueError("[info:get_deviceId] Invalid login hash block")

    devid, hash = loginhashblock.split("$", 1)
    return devid

def create_deviceId(DEBUG=False):
    """
    This function is to make device Id
    :param DEBUG:
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
    This function compare two LHB in Python to check if they are identical.
    :param a: compare login hash block
    :param b: compare login hash block
    :param DEBUG:
    :return: BOOL
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

def valid_loginhashblock(loginhashblock, DEBUG=False):
    """
    This function is to check login hash block
    hashblock format: deviceid(8)+$+hash
    ex)jUs6LQMX$jUs6LQMX$ceccffbfa52e55825f87573b068c8d759b1540f9833a7d7ebd7a27c993ffd316
    :param hashblock:
    :return: BOOL
    """
    if not loginhashblock:
        if DEBUG:
            print('[info:valid_loginhashblock] Null')
        return False

    if loginhashblock.count("$") != 1:
        if DEBUG:
            print('[info:valid_loginhashblock] Invalid format')
        return False

    devid, hash = loginhashblock.split("$", 1)

    if len(devid) != 8:
        if DEBUG:
            print('[info:valid_loginhashblock] Invalid deviceid')
        return False

    if DEBUG:
        print('[info:valid_loginhashblock] login hash block is valid')

    return True

def update_loginhashblock(prev_loginhashblock, DEBUG=False):
    """
    This function is to update login hash block with old login hash block
    :param prev_loginhashblock:
    :param DEBUG:
    :return: updated login hash block
    """

    if not valid_loginhashblock(prev_loginhashblock, DEBUG=DEBUG):
        raise ValueError("[info:update_loginhashblock] Invalid login hash block")

    devid, hash = prev_loginhashblock.split("$", 1)
    loginhashblock = create_loginhashblock(devid, DEBUG=DEBUG)

    if DEBUG:
        text = '[info:update_loginhashblock] \nprev_loginhashblock: {}\n     loginhashblock: {}'.format(prev_loginhashblock,loginhashblock)
        print(text)

    return loginhashblock

def valid_prevloginhashblock(client_loginhashblock, LHBliststr, DEBUG=False):
    """
    This function is to check valid previous login hash block.
    :client_loginhashblock: client's login hash block
    :LHBliststr: client's login has block in database
    """

    server_loginhashblocklist = LHBliststr.split(',')

    if not valid_loginhashblock(client_loginhashblock, DEBUG=DEBUG):
        return False

    devid = get_deviceId(client_loginhashblock, DEBUG=DEBUG)
    server_loginhashblock = get_loginhashblock(devid, server_loginhashblocklist, DEBUG=DEBUG)

    if DEBUG:
        print("[info:valid_loginhashblock]\nclient_loginhashblock: {}\nserver_loginhashblock: {}".format(client_loginhashblock, server_loginhashblock))

    if client_loginhashblock == server_loginhashblock:
        return True

    return False

def get_loginhashblock(devid, loginhashblocklist, DEBUG=False):
    """
    This function is to get login hash block by device id in login hash block list.
    :devid: device id
    :loginhashblocklist: client's login has block in database
    :return:
    """

    for i in loginhashblocklist:
        _devid = get_deviceId(i, DEBUG=DEBUG)
        if devid == _devid:
            if DEBUG:
                print('[info:get_loginhashblock] devid is found in login hash block list')
            return i

    if DEBUG:
        print('[info:get_loginhashblock] devid is not found in login hash block list')

    return False

def create_loginhashblock(devid, key=None, DEBUG=False):
    """
    This functions is to generate login hash block with devid
    :param devid:
    :param key:
    :param DEBUG:
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

    loginhashblock = '{}${}'.format(devid, hash)

    return loginhashblock
