#!/usr/bin/python3
""" finds quilt packages that are mentioned in the documentation,
    then checks if they exist in the public registry
    TODO: add checks for tags/hashes/version """
#
# Travis usage will be:
#
# pip install requirements.txt
# git clone https://github.com/mhassan102/quilt-docs
# cd monitor
# python3 monitor_logs.py
#

import os
import re
from termcolor import colored

# Global vars
CWD = os.getcwd()
REPO_PATH = CWD + '/..'

def check_quilt_log(user_pkg):
    """ Test user_pkg if present in registry """
    #
    # Didn't find quilt log api at https://github.com/quiltdata/python-api
    # so using direct command
    #
    print("**Checking package " + user_pkg + "..")
    retcode = os.system("quilt log "+ user_pkg +" > /dev/null 2>&1")
    if retcode != 0:
        print(colored("Package " + user_pkg + " not exist \n", 'red'))

def main():
    """ Main handler """
    #
    # Start parsing file in docs
    #
    for file in [file_ for file_ in os.listdir(REPO_PATH) if file_.endswith(".md")]:
        with open(os.path.join(REPO_PATH, file)) as file_:
            for line in file_:
                # checking similar lines with 'quilt.data.user import pkg'
                grp = re.search(r'from quilt.(data|vfs)[.]([a-zA-Z0-9_]{4,12}) import ([a-zA-Z0-9_]{4,50})', line)
                if grp:
                    pkg_user = "{}/{}".format(grp.group(2), grp.group(3))
                    check_quilt_log(pkg_user)

                # checking similar lines with 'quilt install user\pkg'
                grp = re.search(r'quilt install ([a-zA-Z0-9_]{4,12})\/([a-zA-Z0-9_]{4,50})', line)
                if grp:
                    pkg_user = "{}/{}".format(grp.group(1), grp.group(2))
                    check_quilt_log(pkg_user)

if __name__ == "__main__":
    main()
