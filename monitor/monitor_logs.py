#!/usr/bin/python3
#
# Travis usage will be: 
#
# pip install requirements.txt 
# git clone https://github.com/mhassan102/quilt-docs
# cd monitor 
# python3 monitor_logs.py
#

import git
import os
import re
#from github import Github

# Global vars
CWD=os.getcwd()
REPO_PATH=CWD + '/..'

def check_quilt_log(user_pkg):
    #
    # Didn't find quilt log api at https://github.com/quiltdata/python-api
    # so using direct command
    #
    print("**Checking package " + user_pkg + "..")
    retcode = os.system("quilt log "+ user_pkg +" > /dev/null 2>&1")
    if ( retcode != 0 ):
        print("Package " + user_pkg + " not exist \n")

def main():
    #
    # main() handler
    #
   
    # Start parsing file in docs
    for file in os.listdir(REPO_PATH):
        if file.endswith(".md"):
            with open(os.path.join(REPO_PATH, file)) as f:
                for line in f:
		    # checking similar lines with 'quilt.data.user import pkg'
                    m = re.search(r'from quilt.(data|vfs).[a-zA-Z0-9_]{4,12} import [a-zA-Z0-9_]{4,50}', line)
                    if m:
                        pkg=m.group(0).split(" ")[3]
                        user=(m.group(0).split(" ")[1]).split(".")[2]
                        pkg_user=user+'/'+pkg
                        check_quilt_log(pkg_user)
	
                    # checking similar lines with 'quilt install user\pkg'
                    m = re.search(r'quilt install [a-zA-Z0-9_]{4,12}\/[a-zA-Z0-9_]{4,50}', line)
                    if m:
                        pkg_user=m.group(0).split(" ")[2]
                        check_quilt_log(pkg_user)

if __name__== "__main__":
    main()
