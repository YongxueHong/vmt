import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])
from base import utils_cmd, user_exception, utils_misc
from platform import machine

color = utils_misc.Colored()
def install_brew(verbose=True):
    status, output = utils_cmd.cmd_status_output(cmd='which brew')
    if verbose:
        print(output)
    if status:
        rel_ver = utils_cmd.cmd_output(
            cmd='cat /etc/redhat-release | '
                'grep -oE \'[0-9]+\.[0-9]+\'| cut -d\'.\' -f1',
            verbose=False)
        status, output = utils_cmd.cmd_status_output('yum install -y brewkoji')
        if verbose:
            print(output)
        if status:
            print(color.red('Failed to install \"brewkoji\"'))
            print(color.red('Please get rcm-tools-rhel-%s-server.repo by manual.'
                                       % rel_ver.rstrip()))
            sys.exit(1)

def brew_download_rpms(rpm_nvr, arch=None, verbose=True):
    download_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 'downloads')
    if not os.path.exists(download_file):
        os.mkdir(download_file)
    if arch:
        dir_rpm = os.path.join(download_file, (rpm_nvr + '.' + arch))
    else:
        dir_rpm = os.path.join(download_file, rpm_nvr)
    if not os.path.exists(dir_rpm):
        os.mkdir(dir_rpm)
    brew_download_cmd = 'cd %s; brew download-build' % dir_rpm
    brew_download_cmd += ' --arch=%s' % arch
    brew_download_cmd += ' ' + ' --noprogress ' + rpm_nvr

    status, output = utils_cmd.cmd_status_output(cmd=brew_download_cmd)
    if verbose:
        print(output)
    if status:
        utils_cmd.cmd_output('rm -rf %s' % dir_rpm, verbose=False)
        print(color.red('Failed to download \"%s\" package.' % rpm_nvr))
        return dir_rpm, False
    return dir_rpm, True

def brew_search(build_pattern):
    output = utils_cmd.cmd_output("brew search build -r %s" % build_pattern)
    build_list = [build for build in output.splitlines()]
    return build_list

if __name__ == "__main__":
    print(brew_search('qemu-kvm-rhev-2.10'))
    pass