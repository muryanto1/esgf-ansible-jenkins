import os
import time
import re
from shutil import copyfile

def update_file(file_to_update, str_to_replace, replacement_str, workdir):

    current_time = time.localtime(time.time())
    time_str = time.strftime("%b.%d.%Y.%H:%M:%S", current_time)
    fname = os.path.basename(file_to_update)
    temp_file_name = "{f}.{d}.txt".format(f=fname, d=time_str)
    temp_file_full_path = os.path.join(workdir, temp_file_name)

    src_f = open(file_to_update, "r")
    temp_file = open(temp_file_full_path, "w+")
    for line in src_f:
        match_str = ".*{s}.*".format(s=str_to_replace)
        match_obj = re.match(match_str, line)
        if match_obj:
            new_line = line.replace(str_to_replace, replacement_str)
            temp_file.write(new_line)
        else:
            temp_file.write(line)
    src_f.close()
    temp_file.close()

    copyfile(temp_file_full_path, file_to_update)
