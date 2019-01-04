import sys
import os
import re

from Util import *

def check_num_of_vm_running(vm_host):

    # check if vm is running
    cmd = "ssh -t jenkins@{h} \"vmrun list\"".format(h=vm_host)
    ret_code, output = run_cmd_capture_output(cmd, True, False, True)

    n_running_vm = 0
    for a_line in output:
        m = re.match(r'Total\s+running\s+VMs:\s+(\d+)', a_line)
        if m:
            n_running_vm = m.group(1)

    return(ret_code, n_running_vm)


def stop_vm_if_running(vm_host, vmx):

    ret_code, n_running_vm = check_num_of_vm_running(vm_host)
    if ret_code != SUCCESS:
        return ret_code

    if n_running_vm == '1':
        print("vm is running... shutting it down")
        cmd = "ssh -t jenkins@{h} \"vmrun stop {vmx}\"".format(h=vm_host,
                                                            vmx=vmx)
        ret_code = run_cmd(cmd, True, False, True)
        if ret_code != SUCCESS:
            print("FAIL...{cmd}".format(cmd=cmd))
            return ret_code

        ret_code, n_running_vm = check_num_of_vm_running(vm_host)                
        print("number of running vm now: " + n_running_vm)

    return ret_code

def revert_vm_to_snapshot(vm_host, vmx, vm_snapshot):

    cmd = "ssh -t jenkins@{h} \"vmrun revertToSnapshot {vmx} {s}\"".format(h=vm_host,
                                                                        vmx=vmx,
                                                                        s=vm_snapshot)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))

    return ret_code
    

def start_vm(vm_host, vmx):
    cmd = "ssh -t jenkins@{h} \"vmrun start {vmx} nogui\"".format(h=vm_host,
                                                               vmx=vmx)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))
        return ret_code

    ret_code, n_running_vm = check_num_of_vm_running(vm_host)                
    print("number of running vm now: " + n_running_vm)
    return(ret_code)

def get_vm_ready(vm_node):
    cmd = "ssh -t jenkins@{n} \"sudo ntpdate -u 0.centos.pool.ntp.org\"".format(n=vm_node)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))

    cmd = "ssh -t jenkins@{n} \"date\"".format(n=vm_node)
    run_cmd(cmd, True, False, True)

    return ret_code

def do_yum_update(vm_node):
    cmd = "ssh -t jenkins@{n} \"sudo yum clean all\"".format(n=vm_node)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))

    cmd = "ssh -t jenkins@{n} \"sudo yum update -y\"".format(n=vm_node)
    run_cmd(cmd, True, False, True)

    return ret_code


