import sys
import os
import argparse
import re

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

#from Util import *
from vm_util import *

parser = argparse.ArgumentParser(description="prepare a virtual machine",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-H", "--vm_host", help="vm_host", required=True)
parser.add_argument("-x", "--vmx", help="full path vmx file name", required=True)
parser.add_argument("-s", "--snapshot", help="vm snapshot to use", required=True)
parser.add_argument("-n", "--vm_node", help="vm node", required=True)
args = parser.parse_args()

vm_host = args.vm_host
vmx = args.vmx
vm_snapshot = args.snapshot
vm_node = args.vm_node

# check if vm is running (note that there may be a vm with different vmx file
# for this vm that is running.
vmx_filename = check_if_vm_is_running(vm_host, vm_node)

# stop vm if running
if vmx_filename is not None:
    ret_code = stop_vm(vm_host, vmx_filename)
    if ret_code != SUCCESS:
        sys.exit(ret_code)

# revert vm to snapshot and start it
ret_code = revert_vm_to_snapshot(vm_host, vmx, vm_snapshot)
if ret_code != SUCCESS:
    sys.exit(ret_code)

ret_code = start_vm(vm_host, vmx)
if ret_code != SUCCESS:
    sys.exit(ret_code)

ret_code = get_vm_ready(vm_node)
if ret_code != SUCCESS:
    sys.exit(ret_code)

#ret_code = do_yum_update(vm_node)

sys.exit(ret_code)

