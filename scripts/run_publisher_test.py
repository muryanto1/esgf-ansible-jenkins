import sys
import os
import argparse

this_dir = os.path.abspath(os.path.dirname(__file__))
modules_dir = os.path.join(this_dir, '..', 'modules')
sys.path.append(modules_dir)

from Util import *

parser = argparse.ArgumentParser(description="run esgf-publisher-test",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-b", "--branch", default='devel', help="git branch of esg-publisher repo, assumes -i")
parser.add_argument("-w", "--workdir", required=True, help="working directory where this script can write to")
parser.add_argument("-e", "--esgf_conda_env", default='esgf-pub', help="esgf conda environment to run test in")
parser.add_argument("-i", "--install", help="Install a new version of the publisher", action="store_true")

args = parser.parse_args()
branch = args.branch
workdir = args.workdir
esgf_conda_env = args.esgf_conda_env

conda_path = "/usr/local/conda/bin"
set_env = "export UVCDAT_ANONYMOUS_LOG=False"

def get_esg_publisher(workdir, env, branch='devel'):

    repo_dir = "{d}/repos".format(d=workdir)
    if os.path.isdir(repo_dir) is False:
        cmd = "mkdir -p {d}".format(d=repo_dir)
        ret_code = run_cmd(cmd, True, False, True)
        if ret_code != SUCCESS:
            print("FAIL...{c}".format(c=cmd))
            return ret_code
    
    the_repo_dir = "{d}/esg-publisher".format(d=repo_dir)
    if os.path.isdir(the_repo_dir) is False:
        cmd = "git clone https://github.com/ESGF/esg-publisher {d}".format(d=the_repo_dir)
        ret_code = run_cmd(cmd, True, False, True)
        if ret_code != SUCCESS:
            print("FAIL...{c}".format(c=cmd))
            return ret_code

    if branch != 'master':
        cmd = "git checkout {b}".format(b=branch)
        ret_code = run_cmd(cmd, True, False, True, the_repo_dir)

    cmd = "git pull"
    ret_code = run_cmd(cmd, True, False, True, "{d}".format(d=the_repo_dir))
    if ret_code != SUCCESS:
        print("FAIL...{c}".format(c=cmd))
        return ret_code

    dir = "{repo_dir}/src/python/esgcet".format(repo_dir=the_repo_dir)
    set_env = "export UVCDAT_ANONYMOUS_LOG=False"
    cmd = "cd {dir}; {set_env}; python setup.py install".format(set_env=set_env,
                                                                dir=dir)

    conda_path = "/usr/local/conda/bin"
    ret_code = run_in_conda_env_as_root(conda_path, env, cmd)
    return(ret_code)

def run_esgf_publisher_test(workdir, esgf_conda_env, unpublish=True):

    print("xxx xxxx in run_esgf_publisher_test xxx")
    repo_dir = "{d}/repos".format(d=workdir)
    the_repo_dir = "{d}/esg-publisher".format(d=repo_dir)

    tmp_dir = "/tmp/"
    dir = "{repo_dir}/src/python/esgcet".format(repo_dir=the_repo_dir)

    # /usr/local/conda/envs/esgf-pub/bin/esgtest_publish
    if unpublish:
        cmd = "{c}/../envs/{env}/bin/esgtest_publish".format(c=conda_path,
                                                             env=esgf_conda_env)
    else:
        cmd = "{c}/../envs/{env}/bin/esgtest_publish -x".format(c=conda_path,
                                                             env=esgf_conda_env)        
    cmd = "cd {dir}; {set_env}; {cmd}".format(dir=tmp_dir,
                                              set_env=set_env,
                                              cmd=cmd)

    ret_code = run_in_conda_env_as_root(conda_path, esgf_conda_env, cmd)
    return(ret_code)

def run_import_test(esgf_conda_env):

    cmd = "{e}; python -c 'import esgcet.config.cmip6_handler'".format(e=set_env)
    ret_code = run_in_conda_env_as_root(conda_path, esgf_conda_env, cmd)
    return(ret_code)

#
# main code
#

exit_status = 0


if (args.install):
    status = get_esg_publisher(workdir, esgf_conda_env, branch)
    if status != SUCCESS:
        print("FAIL FAIL ...get_esg_publisher")
        exit_status |= status

status = run_esgf_publisher_test(workdir, esgf_conda_env)
if status != SUCCESS:
    print("FAIL FAIL...esgtest_publisher")
    exit_status |= status

unpublish = False
status = run_esgf_publisher_test(workdir, esgf_conda_env, unpublish)
if status != SUCCESS:
    print("FAIL FAIL...esgtest_publisher")
    exit_status |= status

status = run_import_test(esgf_conda_env)
if status != SUCCESS:
    print("FAIL FAIL...import test")
    exit_status |= status
sys.exit(exit_status)


