import sys
import os
import re

from Util import *

def check_num_of_vm_running(vm_host):

    # check if vm is running
    cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{h} \"vmrun list\"".format(h=vm_host)
    ret_code, output = run_cmd_capture_output(cmd, True, False, True)

    n_running_vm = 0
    for a_line in output:
        m = re.match(r'Total\s+running\s+VMs:\s+(\d+)', a_line)
        if m:
            n_running_vm = m.group(1)

    return(ret_code, n_running_vm)

def check_if_vm_is_running(vm_host, vm):

    # check if vm is running
    cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{h} \"vmrun list\"".format(h=vm_host)
    ret_code, output = run_cmd_capture_output(cmd, True, False, True)

    vmx_filename = None
    for a_line in output:
        m = re.match(r'Total\s+running\s+VMs:\s+(\d+)', a_line)
        if m:
            n_running_vm = m.group(1)
            if n_running_vm == 0:
                break
        if vm in a_line:
            print("FOUND the vm file: {s}".format(s=a_line))
            vmx_filename = a_line.rstrip()

    return vmx_filename

def stop_vm(vm_host, vmx):

    cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{h} \"vmrun stop {vmx}\"".format(h=vm_host,
                                                           vmx=vmx)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))
    return ret_code

def revert_vm_to_snapshot(vm_host, vmx, vm_snapshot):

    cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{h} \"vmrun revertToSnapshot {vmx} {s}\"".format(h=vm_host,
                                                                        vmx=vmx,
                                                                        s=vm_snapshot)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))

    return ret_code
    
def start_vm(vm_host, vmx):
    cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{h} \"vmrun start {vmx} nogui\"".format(h=vm_host,
                                                               vmx=vmx)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))
    return(ret_code)

def get_vm_ready(vm_node):
    cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{n} \"sudo ntpdate -u 0.centos.pool.ntp.org\"".format(n=vm_node)
    ret_code = run_cmd(cmd, True, False, True)
    if ret_code != SUCCESS:
        print("FAIL...{cmd}".format(cmd=cmd))

    cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{n} \"date\"".format(n=vm_node)
    run_cmd(cmd, True, False, True)

    return ret_code

def do_yum_update(vm_node, module):
    #cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{n} \"sudo yum clean all\"".format(n=vm_node)
    #ret_code = run_cmd(cmd, True, False, True)
    #if ret_code != SUCCESS:
    #    print("FAIL...{cmd}".format(cmd=cmd))

    cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{n} \"sudo yum update -y {m}\"".format(n=vm_node,
                                                                                             m=module)
    run_cmd(cmd, True, False, True)

    return ret_code

def do_yum_install(vm_node, package):
    cmd = "ssh -o StrictHostKeyChecking=no -t jenkins@{n} \"sudo yum -y install {p}\"".format(n=vm_node,
                                                                                              p=package)
    run_cmd(cmd, True, False, True)

    return ret_code




