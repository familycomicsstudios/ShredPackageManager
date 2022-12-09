#!/usr/bin/env python3

#Imports
import argparse
import os, sys
import requests
import json
import flask
from flask import redirect, request

#Argument Parsing

parser = argparse.ArgumentParser(prog = 'shpm', description='Scratch extension package manager', epilog='This version of shpm has Super Sus Powers.')
parser.add_argument("cmd", help="The command you use", nargs='?', default = '')
parser.add_argument("extra", help="Extra parameter", nargs="?",default='')
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=True)
group.add_argument("-q", "--quiet", help="Do run quietly", action="store_true")
parser.add_argument("-d", "--dry", help="Do a dry run", action="store_true")
parser.add_argument("-A", "--amogus", help="Hmmmmmmm", action="store_true")
parser.add_argument("-l", "--local", help="Install package from local file", action="store_true")
args = parser.parse_args()

#PWD stuff

from os import listdir
from os.path import isfile, join
mypath = os.getcwd()+"/.scratch-modules"
try:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
except:
    pass
workdir = os.getcwd()

#Metadata

version = '0.3.0'

#Flagset

verbose = args.verbose and not args.quiet
dry = args.dry

#Flask

app = flask.Flask(__name__,
            static_url_path='', 
            static_folder=workdir+'.scratch-modules')

@app.route('/')
def main():
    global onlyfiles
    url = 'https://turbowarp.org'
    if len(onlyfiles) > 0:
        url += '?extension=https://'+request.host+'/modules/'+onlyfiles[0]
        fileno = 1
        for file in onlyfiles[1:]:
            url += '&extension=https://'+request.host+'/modules/'+onlyfiles[fileno]
            fileno += 1
            
    return redirect(url)

from flask import send_from_directory

@app.route('/modules/<path>')
def send_report(path):
    return open('.scratch-modules/'+path, 'r').read()

#Functions

def init():
    global verbose, dry
    if not dry:
        os.mkdir(".scratch-modules")
    if verbose:
        print("INFO || Making modules directory.")

def update_repo():
    global verbose, dry
    url = 'https://familycomicsstudios.github.io/ShredRepository/packages.json'
    if verbose:
        print("INFO || Getting repositories list.")
    r = requests.get(url, allow_redirects=True)
    if not dry:
        open('packages.json', 'wb').write(r.content)
    if verbose:
        print("INFO || Finished!")

def get_package(package):
    global verbose, dry, args
    if args.local:
        r = open(package, 'r').read()
    else:
        if verbose:
            print("INFO || Searching repositories list.")
        try:
            with open('packages.json', 'r') as fcc_file:
                url = json.load(fcc_file)[package]['repository_reqget']
        except:
            print("ERROR || Nonexistent package. Exiting.", file=sys.stderr)
            return
        if verbose:
            print("INFO || Getting package.")
        r = requests.get(url, allow_redirects=True)
    os.chdir(".scratch-modules")
    if verbose:
        print("INFO || Installing package.")
    if not dry:
        open(package+'.js', 'wb').write(r.content)
    if verbose:
        print("INFO || Finished!")

def package_list(search):
    global verbose
    if verbose:
        print("INFO || Searching repositories list.")
    with open('packages.json', 'r') as fcc_file:
        for key in json.load(fcc_file).keys():
            if search in key:
                print(key)
    

def start_server():
    if verbose:
        print("INFO || Starting server.")
    app.run(host="0.0.0.0", port=8000)

def get_package_info(package):
    global verbose, dry
    if verbose:
        print("INFO || Searching repositories list.")
    try:
        with open('packages.json', 'r') as fcc_file:
            jsont = json.load(fcc_file)[package]
    except:
        print("ERROR || Nonexistent package. Exiting.", file=sys.stderr)
        return
    print("Name:",jsont["name"])
    print("Description:",jsont["description"])
    print("Author:",jsont["author_name"])
    print("Contact:",jsont["author_contact"])
    print("Version:",jsont["version"])
    print("Sandboxed:",jsont["sandboxed"])
    if verbose:
        print("INFO || Done!")

def amogus():
    print("""
                                            
                                        
                                        
               (@@@@@@@@@@@.            
             #@@%%%%%%%%%%&@@@          
            @@@%%%%@@@@@@@@@@@@@        
            @@&%%%@@#,,,      ,@@/      
       @@@@@@@&%%%@@##(,,,,,,,*#@@.     
      *@@%%%@@&%%%&@@#########%@@#      
      *@@&&&@@&%%%%%%@@@@@@@&%%@%       
      (@&&&&@@&&%%%%%%%%%%%%%%&@@       
      (@&&&&@@&&&%%%%%%%%%%%%%&@@       
      (@&&&&@@&&&&&%%%%%%%%%&&&@&       
       @@&&&@@&&&&&&&&&&&&&&&&@@*       
         /%@@@&&&&&&@@@@@@&&&&@@        
            @@&&&&&&@@ @@&&&&@@#        
            @@@&&&@@@.  &@@@@@.         
               .,,                      
                                        
            sus amognus                            
    """)

def remove_package(package):
    global verbose, dry
    if verbose:
        print("INFO || Changing directory to extensions folder.")
    os.chdir(".scratch-modules")
    if verbose:
        print("INFO || Uninstalling package.")
    if not dry:
        try:
            os.remove(package+'.js')
        except:
            print("ERROR || Package not existent.", file=sys.stderr)
    if verbose:
        print("INFO || Finished!")

def list():
    if verbose:
        print("INFO || Listing directory...")
    for item in onlyfiles:
        print(item)
    if verbose:
        print("INFO || Done!")
        
# Main

if args.cmd == "init":
    init()
elif args.cmd == "update":
    update_repo()
elif args.cmd == "install" or args.cmd == "i":
    get_package(args.extra)
elif args.cmd == "start":
    start_server()
elif args.cmd == "search":
    package_list(args.extra)
elif args.cmd == "version":
    print(version)
elif args.cmd == "info":
    get_package_info(args.extra)
elif args.cmd == "uninstall" or args.cmd == "remove" or args.cmd == "ui":
    remove_package(args.extra)
elif args.cmd == "list" or args.cmd == "l":
    list()
elif args.amogus:
    amogus()
else:
    print("ERROR || No valid command selected. Exiting.", file=sys.stderr)
    parser.print_usage()
