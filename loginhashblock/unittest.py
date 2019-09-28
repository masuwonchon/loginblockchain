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

DEBUG = False
unittest_update_loginhashblocklist()
unittest_create_loginhashblocklist()