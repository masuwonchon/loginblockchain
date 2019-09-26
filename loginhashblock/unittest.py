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

def cprint(message):
    print(bcolors.WARNING + message + bcolors.ENDC)

def unittest_01():
    pre_loginhashblock = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    pre_loginhashblocklist = ''

    new_loginhashblock = update_loginhashblock(pre_loginhashblock, DEBUG=DEBUG)
    new_loginhashblocklist = update_loginhashblocklist(pre_loginhashblocklist, new_loginhashblock, DEBUG=DEBUG)

    if new_loginhashblocklist == new_loginhashblock:
        cprint("unittest_01: Success")
    else:
        cprint("unittest_01: Fail")

    pre_loginhashblocklist = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2,aCIXQRZ2$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a3'
    new_loginhashblock = update_loginhashblock(pre_loginhashblock, DEBUG=DEBUG)
    new_loginhashblocklist = update_loginhashblocklist(pre_loginhashblocklist, new_loginhashblock, DEBUG=DEBUG)
    res = pre_loginhashblocklist.split(',')

    if new_loginhashblocklist == '{},{}'.format(new_loginhashblock, res[1]):
        cprint("unittest_01: Success")
    else:
        cprint("unittest_01: Fail")

    pre_loginhashblocklist = ''
    new_loginhashblock = update_loginhashblock(pre_loginhashblock, DEBUG=DEBUG)
    new_loginhashblocklist = update_loginhashblocklist(pre_loginhashblocklist, new_loginhashblock, DEBUG=DEBUG)

    if new_loginhashblocklist == new_loginhashblock:
        cprint("unittest_01: Success")
    else:
        cprint("unittest_01: Fail")

    pre_loginhashblocklist = 'aCIXQRZ2$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2,aCIXQRZ3$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a3'
    new_loginhashblock = update_loginhashblock(pre_loginhashblock, DEBUG=DEBUG)
    new_loginhashblocklist = update_loginhashblocklist(pre_loginhashblocklist, new_loginhashblock, DEBUG=DEBUG)
    res = pre_loginhashblocklist.split(',')

    if new_loginhashblocklist == '{},{}'.format(pre_loginhashblocklist, new_loginhashblock):
        cprint("unittest_01: Success")
    else:
        cprint("unittest_01: Fail")

def unittest_02():
    # case 01
    prev_LHB = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a1'
    LHBlistStr = ''

    NewLHBlistStr = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)

    source = prev_LHB.split('$')
    target = NewLHBlistStr.split('$')

    if source[0] == target[0] and source[1] != target[1]:
        cprint("unittest_02-01: Success")
    else:
        cprint("unittest_02-01: Fail")

    # case 02
    LHBlistStr = 'aCIXQRZ1$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2,aCIXQRZ2$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a3'

    LHBlist = LHBlistStr.split(',')
    NewLHBlistStr = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)
    targetList = NewLHBlistStr.split(',')
    target = targetList[0].split('$')

    if source[0] == target[0] and source[1] != target[1] and LHBlist[1] == targetList[1]:
        cprint("unittest_02-02: Success")
    else:
        cprint("unittest_02-02: Fail")

    if LHBlistStr != NewLHBlistStr:
        cprint("unittest_02-03: Success")
    else:
        cprint("unittest_02-03: Fail")

    # case 03
    LHBlistStr = 'aCIXQRZ3$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'

    LHBlist = LHBlistStr.split(',')
    NewLHBlistStr = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)
    targetList = NewLHBlistStr.split(',')
    target = targetList[1].split('$')

    if source[0] == target[0] and source[1] != target[1]:
        cprint("unittest_02-04: Success")
    else:
        cprint("unittest_02-04: Fail")

    if LHBlistStr != NewLHBlistStr:
        cprint("unittest_02-05: Success")
    else:
        cprint("unittest_02-05: Fail")

    if len(targetList) == 2:
        cprint("unittest_02-06: Success")
    else:
        cprint("unittest_02-06: Fail")

    # case 04
    prev_LHB = ''
    LHBlistStr = 'aCIXQRZ3$2b76784270f608bedf2757113041a6f6e81ab55faf787afde4e57e4376d302a2'

    LHBlist = LHBlistStr.split(',')
    NewLHBlistStr = update_loginhashblocklist(LHBlistStr, prev_LHB, DEBUG=DEBUG)
    targetList = NewLHBlistStr.split(',')

    if LHBlistStr == NewLHBlistStr:
        cprint("unittest_02-07: Success")
    else:
        cprint("unittest_02-07: Fail")

    if len(targetList) == 1:
        cprint("unittest_02-08: Success")
    else:
        cprint("unittest_02-08: Fail")

#unittest_01()
DEBUG = False
unittest_02()
