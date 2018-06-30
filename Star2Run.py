import os
import sys
import logging
from base import utils_brew, utils_cmd, utils_misc
from sys import version_info
from collections import OrderedDict
from platform import machine
from base import options_func

color = utils_misc.Colored()
def create_opt_desc():
    dict = OrderedDict()
    dict['1'] = 'Setup network.'
    dict['2'] = 'Search package.'
    dict['3'] = 'Download package.'
    dict['4'] = 'Install qemu package.'
    dict['5'] = 'Setup iSCSI server.'
    dict['6'] = 'Setup Ceph server.'
    dict['7'] = 'Download and bootstrap ipa.'
    dict['l'] = 'List menu.'
    dict['q'] = 'Quit.'
    return dict


def main_loop(dict):
    utils_brew.install_brew(verbose=False)
    while 1:
        opt = utils_misc.py2_and_py3_input()
        # Setup network
        if opt == '1':
            options_func.option_1()
        # Search build
        elif opt == '2':
            options_func.option_2()
        # Download build
        elif opt == '3':
            options_func.option_3()
        # Install qemu package
        elif opt == '4':
            options_func.option_4()
        # Setup iSCSI server
        elif opt == '5':
            options_func.option_5()
        # Setup Ceph server
        elif opt == '6':
            options_func.option_6()
        # Download and bootstrap ipa
        elif opt == '7':
            options_func.option_7()
        elif opt == 'l':
            utils_misc.usage(dict)
        elif opt not in opt_dict:
            print(color.yellow('No this option, please check it again.'))
        elif opt == 'q':
            break

if __name__ == "__main__":
    opt_dict = create_opt_desc()
    utils_misc.usage(opt_dict)
    main_loop(opt_dict)
    try:
        sys.exit(0)
    except:
        print(color.yellow('Quit Virt Mini Toolkit.'))
    finally:
        print(color.yellow('Bye bye !!!'))