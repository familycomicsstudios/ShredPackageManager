#!/usr/bin/env python3

#Imports
import argparse
import os
import requests

#Argument Parsing

parser = argparse.ArgumentParser()
parser.add_argument("cmd", help="The command you use")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

#Flagset

verbose = args.verbose

#Functions

def init():
    global verbose
    os.mkdir(".scratch-modules")
    if verbose:
        print("INFO || Making modules directory.")

def update_repo():
    global verbose
    url = 'https://www.facebook.com/favicon.ico'
    r = requests.get(url, allow_redirects=True)

    open('packages.json', 'wb').write(r.content)
# Main

if args.cmd == "init":
    init()
if args.cmd == "update":
    update_repo()
    