import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])
import time
import subprocess
from base import user_exception, utils_misc
import re
from sys import version_info


def getstatusoutput(cmd, timeout=600):
    """Return (exitcode, output) of executing cmd in a shell.

    Execute the string 'cmd' in a shell with 'check_output' and
    return a 2-tuple (status, output). The locale encoding is used
    to decode the output and process newlines.

    A trailing newline is stripped from the output.
    The exit status for the command can be interpreted
    according to the rules for the function 'wait'. Example:
    """
    try:
        if version_info.major == 3:
            data = subprocess.check_output(cmd, timeout=timeout, shell=True,
                                           universal_newlines=True,
                                           stderr=subprocess.STDOUT)
        elif version_info.major == 2:
            # No argument timeout in check_output with python2.
            data = subprocess.check_output(cmd, shell=True,
                                           universal_newlines=True,
                                           stderr=subprocess.STDOUT)
        exitcode = 0
    except subprocess.CalledProcessError as ex:
        data = ex.output
        exitcode = ex.returncode
    if data[-1:] == '\n':
        data = data[:-1]
    return exitcode, data

def cmd_output(cmd, timeout=300, verbose=True):
    deadline = time.time() + timeout
    if verbose == True:
        print("Sending command: %s" % cmd)
    if version_info.major == 2:
        sub = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while sub.poll() == None:
            if time.time() > deadline:
                err_info = 'Failed to run \"%s\" under %s sec.' % (cmd, timeout)
                raise user_exception.Error(err_info)

        try:
            outs, errs = sub.communicate()
        except ValueError:
            pass

        return utils_misc.convert_to_str(outs + errs)

    elif version_info.major == 3:
        sub = subprocess.run(cmd, timeout=timeout, shell=True,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        return utils_misc.convert_to_str(sub.stdout)


def cmd_status_output(cmd, timeout=600, verbose=True):
    if verbose == True:
        print("Sending command: %s" % cmd)
    return getstatusoutput(cmd, timeout)


if __name__ == "__main__":
    print(cmd_output('uname -r'))
    print(cmd_output('df -h'))
    print(cmd_output('dd if=/dev/urandom of=/tmp/test0 bs=512b count=1000 oflag=direct', 10))
    status, output = cmd_status_output('fdisk -h')
    print(output)
    if status:
        raise user_exception.Error('Command Error')

    status, output = cmd_status_output(
        'dd if=/dev/urandom of=/tmp/test1 bs=512b count=1000 oflag=direct', 5)
    print(output)
    if status:
        raise user_exception.Error('Command error')

    status, output = cmd_status_output('fdik -h')
    print(output)
    if status:
        raise user_exception.Error('Command Error')
    pass
