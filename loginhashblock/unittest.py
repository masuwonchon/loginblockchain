from loginhashblock import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

DEBUG = False

def unittest_print(message):
    print(bcolors.WARNING + message + bcolors.ENDC)

def unittest_title_print(message):
    print(bcolors.OKGREEN + message + bcolors.ENDC)

def unittest_update_loginhashblocklist():
    # case 01
    prev_LHB = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    LHBlistStr = ''

    updatedLHBlistStr, LHBstr = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)

    source = prev_LHB.split('$')
    target = updatedLHBlistStr.split('$')

    unittest_title_print("LHB is one, LHBlist is null")
    if source[0] == target[0] and source[1] != target[1]:
        unittest_print("TestCase-01: Success")
    else:
        unittest_print("TestCase-01: Fail")

    # case 02
    LHBlistStr = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2,aCIXQRZ2$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a3'

    LHBlist = LHBlistStr.split(',')
    updatedLHBlistStr, LHBstr = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)
    targetList = updatedLHBlistStr.split(',')
    target = targetList[0].split('$')

    unittest_title_print("LHB is one, LHBlist is two")
    if source[0] == target[0] and source[1] != target[1] and LHBlist[1] == targetList[1]:
        unittest_print("TestCase-01: Success")
    else:
        unittest_print("TestCase-01: Fail")

    if LHBlistStr != updatedLHBlistStr:
        unittest_print("TestCase-02: Success")
    else:
        unittest_print("TestCase-02: Fail")

    # case 03
    LHBlistStr = 'aCIXQRZ3$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'

    LHBlist = LHBlistStr.split(',')
    updatedLHBlistStr, LHBstr = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)
    targetList = updatedLHBlistStr.split(',')
    target = targetList[1].split('$')

    unittest_title_print("LHB is one, LHBlist is one, but devid is different so LHBlist will be updated LHB")
    if source[0] == target[0] and source[1] != target[1]:
        unittest_print("TestCase-01: Success")
    else:
        unittest_print("TestCase-01: Fail")

    if LHBlistStr != updatedLHBlistStr:
        unittest_print("TestCase-02: Success")
    else:
        unittest_print("TestCase-02: Fail")

    if len(targetList) == 2:
        unittest_print("TestCase-03: Success")
    else:
        unittest_print("TestCase-03: Fail")

    # case 04
    prev_LHB = ''
    LHBlistStr = 'aCIXQRZ3$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'

    LHBlist = LHBlistStr.split(',')
    updatedLHBlistStr, LHBstr = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)
    targetList = updatedLHBlistStr.split(',')

    unittest_title_print("LHB is null, LHBlist is one, su LHBlist will be maintained")
    if LHBlistStr == updatedLHBlistStr:
        unittest_print("TestCase-01: Success")
    else:
        unittest_print("TestCase-01: Fail")

    if len(targetList) == 1:
        unittest_print("TestCase-02: Success")
    else:
        unittest_print("TestCase-02: Fail")

def unittest_create_loginhashblocklist():

    LHBlistStr = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'

    updatedLHBlistStr, LHBstr = create_loginhashblocklist(LHBlistStr, DEBUG=DEBUG)
    LHBlist = updatedLHBlistStr.split(',')

    ("Create LHB and updated LHBlistStr")
    if len(LHBlist) == 2:
        unittest_print("TestCase-01: Success")
    else:
        unittest_print("TestCase-01: Fail")

    if LHBlist[0] == LHBlistStr:
        unittest_print("TestCase-02: Success")
    else:
        unittest_print("TestCase-02: Fail")

def unittest_request_login_token():
    unittest_title_print("unittest request login with token")
    LHBlistStr = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    prev_LHB = ''
    token='123456'
    verify_totp = False
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    if ret == 1:
        unittest_print("TestCase-01: Success")
    else:
        unittest_print("TestCase-01: Fail")

    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    LHBlist = updatedLHBlistStr.split(',')
    if LHBlist[0] == LHBlistStr:
        unittest_print("TestCase-02: Success")
    else:
        unittest_print("TestCase-02: Fail")

    if len(LHBlist)  == 2:
        unittest_print("TestCase-03: Success")
    else:
        unittest_print("TestCase-03: Fail")

    prev_LHB = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    if ret == 2:
        unittest_print("TestCase-04: Success")
    else:
        unittest_print("TestCase-04: Fail")

    prev_LHB = 'aCIXQRZ11$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    if ret == 2:
        unittest_print("TestCase-05: Success")
    else:
        unittest_print("TestCase-05: Fail")

    prev_LHB = 'aCIXQRZ11$$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    if ret == 2:
        unittest_print("TestCase-05: Success")
    else:
        unittest_print("TestCase-05: Fail")

    prev_LHB = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)
    updatedLHBlist = updatedLHBlistStr.split(',')

    if LHBlistStr != updatedLHBlist[0]:
        unittest_print("TestCase-06: Success")
    else:
        unittest_print("TestCase-06: Fail")

    prev_LHB = 'aCIXQRZ2$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)
    updatedLHBlist = updatedLHBlistStr.split(',')

    if len(updatedLHBlist) == 2:
        unittest_print("TestCase-07: Success")
    else:
        unittest_print("TestCase-07: Fail")

    prev_LHB = 'aCIXQRZ2$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)
    updatedLHBlist = updatedLHBlistStr.split(',')

    if len(updatedLHBlist) == 2:
        unittest_print("TestCase-07: Success")
    else:
        unittest_print("TestCase-07: Fail")

    devid = get_deviceId(updatedLHBlist[1], DEBUG=False)
    devid_ = get_deviceId(prev_LHB, DEBUG=False)

    if devid == devid_:
        unittest_print("TestCase-08: Success")
    else:
        unittest_print("TestCase-08: Fail")

    LHBlistStr = ''
    prev_LHB = ''
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)
    updatedLHBlist = updatedLHBlistStr.split(',')

    if len(updatedLHBlist) == 1:
        unittest_print("TestCase-09: Success")
    else:
        unittest_print("TestCase-09: Fail")

def unittest_request_login_notoken():
    unittest_title_print("unittest request login with no token")
    LHBlistStr = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    prev_LHB = ''
    token=''
    verify_totp = False
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    if ret == 5:
        unittest_print("TestCase-01: Success")
    else:
        unittest_print("TestCase-01: Fail")

    prev_LHB = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    if ret  == 4:
        unittest_print("TestCase-02: Success")
    else:
        unittest_print("TestCase-02: Fail")

    prev_LHB = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    if ret == 3:
        unittest_print("TestCase-03: Success")
    else:
        unittest_print("TestCase-03: Fail")

    prev_LHB = 'aCIXQRZ11$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    if ret == 3:
        unittest_print("TestCase-04: Success")
    else:
        unittest_print("TestCase-04: Fail")

    prev_LHB = 'aCIXQRZ11$$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)

    if ret == 3:
        unittest_print("TestCase-05: Success")
    else:
        unittest_print("TestCase-05: Fail")

    prev_LHB = 'aCIXQRZ2$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)
    updatedLHBlist = updatedLHBlistStr.split(',')

    if ret == 4:
        unittest_print("TestCase-06: Success")
    else:
        unittest_print("TestCase-06: Fail")

    prev_LHB   = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    verify_totp = True
    updatedLHBlistStr, LHBstr, ret = mok_request_post(token, prev_LHB, verify_totp, LHBlistStr)
    updatedLHBlist = updatedLHBlistStr.split(',')

    if len(updatedLHBlist) == 1:
        unittest_print("TestCase-07: Success")
    else:
        unittest_print("TestCase-07: Fail")

    devid = get_deviceId(updatedLHBlist[0], DEBUG=False)
    devid_ = get_deviceId(prev_LHB, DEBUG=False)

    if devid == devid_:
        unittest_print("TestCase-08: Success")
    else:
        unittest_print("TestCase-08: Fail")

def mok_request_post(token, prev_LHB, verify_totp, LHBlistStr):
    status = 0
    new_LHB = ''

    if token:
        if not verify_totp:
            return LHBlistStr, new_LHB, 1

        if prev_LHB:
            if not valid_loginhashblock(prev_LHB):
                return LHBlistStr, new_LHB, 2

            LHBlistStr, new_LHB = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)
        else:
            LHBlistStr, new_LHB = create_loginhashblocklist(LHBlistStr, DEBUG=DEBUG)
    else:
        if prev_LHB:
            if not valid_loginhashblock(prev_LHB):
                return LHBlistStr, new_LHB, 3

            if not verify_loginhashblock(LHBlistStr, prev_LHB):
                return LHBlistStr, new_LHB, 4

            LHBlistStr, new_LHB = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)
        else:
            return LHBlistStr, new_LHB, 5

    LHBlistStr = LHBlistStr

    return LHBlistStr, new_LHB, status

DEBUG = False

def unittest_subfunction_update_loginhashblock():
    unittest_title_print("unittest sub function update_loginhashblock")
    LHBlistStr = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    prevLHBstr   = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'
    LHBlistStr, LHBstr = update_loginhashblocklist(LHBlistStr, prevLHBstr, DEBUG=False)
    '''
    print("LHBlistStr: {}".format(LHBlistStr))
    print("LHBstr: {}".format(LHBstr))
    '''


unittest_update_loginhashblocklist()
unittest_create_loginhashblocklist()
unittest_request_login_token()
unittest_request_login_notoken()
unittest_subfunction_update_loginhashblock()