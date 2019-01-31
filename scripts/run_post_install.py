import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *
from MiscUtil import *
from vm_util import *

parser = argparse.ArgumentParser(description="run esgf 2.x post install steps",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-H", "--vm_jenkins_home", required=True, help="vm user jenkins home directory")

args = parser.parse_args()
workdir = args.vm_jenkins_home

sys.stdout.flush()

#
# run this on vm node as user 'jenkins'
#


#
# update /usr/local/cog/cog_config/cog_settings.cfg
#
print("xxx DEBUG...going to update cog_settings.cfg to set USE_CAPTCHA to False")
file_to_update = '/usr/local/cog/cog_config/cog_settings.cfg'
var_val_pairs_list = ['USE_CAPTCHA=False']
status = update_cog_settings_conf(var_val_pairs_list, '=', workdir)

if status != 0:
    print("FAIL...update_cog_settings_conf ... for setting USE_CAPTCHA=False")
    sys.exit(status)

sys.exit(status)
#status = do_yum_update(vm_node, 'libarchive-devel')
