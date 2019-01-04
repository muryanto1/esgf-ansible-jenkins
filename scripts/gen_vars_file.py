import os
import sys
import argparse
from shutil import copyfile

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from MiscUtil import update_file


parser = argparse.ArgumentParser(description="generate vars file for running ansible-playbook",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-f", "--vars_file", help="template vars file")
parser.add_argument("-s", "--ssh_passwd", help="ssh passwd")
parser.add_argument("-a", "--admin_passwd", help="admin passwd")
parser.add_argument("-w", "--workdir", help="work directory")
parser.add_argument("-u", "--globus_user", help="globus user")
parser.add_argument("-p", "--globus_passwd", help="globus passwd")


args = parser.parse_args()
vars_file = args.vars_file
ssh_passwd = args.ssh_passwd
admin_passwd = args.admin_passwd
workdir = args.workdir
globus_user = args.globus_user
globus_passwd = args.globus_passwd


vars_file_name = os.path.basename(vars_file)
modified_vars_file = os.path.join(workdir, vars_file_name)
copyfile(vars_file, modified_vars_file)

with open(modified_vars_file, 'a') as f:
    f.write("ansible_ssh_pass: {s}\n".format(s=ssh_passwd))
    f.write("admin_pass: {s}\n".format(s=admin_passwd))
    f.write("globus_user: {s}\n".format(s=globus_user))
    f.write("globus_passwd: {s}\n".format(s=globus_passwd))

copyfile(modified_vars_file, vars_file)
sys.exit(0)
