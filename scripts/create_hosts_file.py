import sys
import os
import argparse

parser = argparse.ArgumentParser(description="create hosts file for ansible-playbook",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-d", "--data_node", required=True, 
                    help="hostname for data node")
parser.add_argument("-i", "--index_idp_node", required=True, 
                    help="hostname for index and idp node")
parser.add_argument("-o", "--host_file", required=True, 
                    help="created host file name")

args = parser.parse_args()
data_node = args.data_node
index_idp_node = args.index_idp_node
host_file = args.host_file

#    [data]
#    myhost.my.org
#
#    [index]
#    myhost.my.org
#
#    [idp]
#    myhost.my.org

with open(host_file, 'w') as out_file:
    out_file.write("[data]\n")
    out_file.write(data_node + "\n\n")
    out_file.write("[index]\n" )
    out_file.write(index_idp_node + "\n\n")
    out_file.write("[idp]\n")
    out_file.write(index_idp_node + "\n\n")

sys.exit(0)

