import sys
import os
import argparse

parser = argparse.ArgumentParser(description="create hosts file for ansible-playbook",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-d", "--data_node", required=True, 
                    help="hostname for data node")
parser.add_argument("-i", "--index_idp_node", required=True, 
                    help="hostname for index and idp node")
parser.add_argument("-s", "--sample_host_file", required=True, 
                    help="sample host file name")
parser.add_argument("-o", "--host_file", required=True, 
                    help="created host file name")

args = parser.parse_args()
data_node = args.data_node
index_idp_node = args.index_idp_node
sample_host_file = args.sample_host_file
host_file = args.host_file

replace_dict = {
    "host-data.my.org" : data_node,
    "host-index-idp.my.org" : index_idp_node,
    }

with open(sample_host_file, 'r') as orig_file:
    lines = orig_file.readlines()

with open(host_file, 'w') as out_file:
    for line in lines:
        replaced = False
        for key in replace_dict:
            if key in line and replaced == False:
                out_file.write(line.replace(key, replace_dict[key]))
                replaced = True
                #break
        if replaced == False:
            out_file.write(line)

sys.exit(0)

