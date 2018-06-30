import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])
from platform import machine
from base import utils_misc, utils_cmd, utils_brew
from collections import defaultdict

color = utils_misc.Colored()
def install_qemu_package(nvr):
    found = False
    download_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 'downloads')
    if os.path.exists(download_file):
        for pkg in os.listdir(download_file):
            if pkg == (nvr + '.' + machine()):
                found = True
                break
        if found:
            utils_cmd.cmd_output('yum remove -y qemu-*')
            utils_cmd.cmd_output('cd %s;yum install -y *' %
                                 (os.path.join(download_file, pkg)))
        else:
            download_dir, ret = utils_brew.brew_download_rpms(rpm_nvr=nvr,
                                                              arch=machine())
            if not ret:
                return  False
            utils_cmd.cmd_output('yum remove -y qemu-*')
            utils_cmd.cmd_output('cd %s;yum install -y *' % download_dir)
    else:
        download_dir, ret = utils_brew.brew_download_rpms(rpm_nvr=nvr,
                                                          arch=machine())
        if not ret:
            return False
        utils_cmd.cmd_output('yum remove -y qemu-*')
        utils_cmd.cmd_output('cd %s;yum install -y *' % download_dir)
    s, o = utils_cmd.cmd_status_output('/usr/libexec/qemu-kvm --version')
    print(o)
    if s !=0:
        print(color.red('Failed to install qemu package.'))
        return False
    else:
        return True

def create_qemu_ifup_script(bridge_iface):
    utils_cmd.cmd_output('echo \"#!/bin/sh\nswitch=%s\n/sbin/ifconfig \$1 0.0.0.0 up\n'
                         '/usr/sbin/brctl addif \${switch} \$1\n'
                         '/usr/sbin/brctl setfd \${switch} 0\n'
                         '/usr/sbin/brctl stp \${switch} off\" > /etc/qemu-ifup'
                         % bridge_iface)
    utils_cmd.cmd_output('chmod 777 /etc/qemu-ifup')

def create_qemu_ifdown_script(bridge_iface):
    utils_cmd.cmd_output('echo \"#!/bin/sh\nswitch=%s\n/sbin/ifconfig \$1 0.0.0.0 down\n'
                         '/usr/sbin/brctl delif \${switch} \$1\" > /etc/qemu-ifdown'
                         % bridge_iface)
    utils_cmd.cmd_output('chmod 777 /etc/qemu-ifdown')

def option_1():
    status, output = utils_cmd.cmd_status_output(cmd='which bridge-utils')
    if status:
        utils_cmd.cmd_status_output(cmd='yum install -y bridge-utils')
    inface = utils_cmd.cmd_output(cmd='ip route | grep default '
                                          '| awk \'{print $5}\' | head -n 1')
    if inface not in utils_cmd.cmd_output(cmd='brctl show | awk \'{print $4}\''):
        utils_cmd.cmd_output('sed -i \'s/^BOOTPROTO=dhcp$/BOOTPROTO=none/g\' '
                             '/etc/sysconfig/network-scripts/ifcfg-%s'
                             % inface)
        utils_cmd.cmd_output('sed -i \'s/^BOOTPROTO="dhcp"$/BOOTPROTO="none"/g\''
                             ' /etc/sysconfig/network-scripts/ifcfg-%s'
                             % inface)
        utils_cmd.cmd_output('echo \"BRIDGE=switch\"'
                             '>>/etc/sysconfig/network-scripts/ifcfg-%s'
                             % inface)
        utils_cmd.cmd_output('echo \"DEVICE=switch\nBOOTPROTO=dhcp\n'
                             'ONBOOT=yes\nTYPE=Bridge\"'
                             '>/etc/sysconfig/network-scripts/ifcfg-switch')
        s, o = utils_cmd.cmd_status_output('service network restart')
        if s != 0:
            print(color.red('Failed to set up network.'))
    create_qemu_ifup_script('switch')
    create_qemu_ifdown_script('switch')

def option_2():
    build = utils_misc.py2_and_py3_input('Please input build searched: ')
    brew_list = utils_brew.brew_search(build)
    for idx, desc in enumerate(sorted(brew_list)):
        print('%d: %s' % (idx + 1, desc))

def option_3():
    nvr = utils_misc.py2_and_py3_input('Please input package '
                                       'name version release(NVR) downloaded: ')
    download_dir, ret = utils_brew.brew_download_rpms(rpm_nvr=nvr,
                                                 arch=machine())
    if not ret:
        print(color.red('Please check package NVR or '
                        'search it before download.'))


def option_4():
    while 1:
        qemu_nvr = utils_misc.py2_and_py3_input(
            'Please input package name version release(NVR) installed: ')
        if not qemu_nvr or not install_qemu_package(qemu_nvr):
            print(color.red('Please check qemu NVR or '
                            'search it before download.'))
            continue
        else:
            break

def option_5():
    print('TODO')
    pass

def option_6():
    print('TODO')
    pass

def option_7():
    print('TODO')
    pass

if __name__ == "__main__":
    # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # kar_loopcase()
    create_qemu_ifdown_script('switch')
    create_qemu_ifup_script('switch')