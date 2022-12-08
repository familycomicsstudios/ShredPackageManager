#!/usr/bin/env python3

#Imports
import argparse
import os
import requests
import json
import flask
from flask import redirect, request

#Argument Parsing

parser = argparse.ArgumentParser(prog = 'shpm')
parser.add_argument("cmd", help="The command you use")
parser.add_argument("extra", help="Extra parameter", nargs="?",default=None)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

#PWD stuff

from os import listdir
from os.path import isfile, join
mypath = os.getcwd()+"/.scratch-modules"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

workdir = os.getcwd()

#Flagset

verbose = args.verbose

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
    global verbose
    os.mkdir(".scratch-modules")
    if verbose:
        print("INFO || Making modules directory.")

def update_repo():
    global verbose
    url = 'https://raw.githubusercontent.com/familycomicsstudios/ShredPackageManager/main/packages.json'
    if verbose:
        print("INFO || Getting repositories list.")
    r = requests.get(url, allow_redirects=True)
    open('packages.json', 'wb').write(r.content)
    if verbose:
        print("INFO || Finished!")

def get_package(package):
    global verbose
    if verbose:
        print("INFO || Searching repositories list.")
    with open('packages.json', 'r') as fcc_file:
        url = json.load(fcc_file)[package]['repository_reqget']
    if verbose:
        print("INFO || Getting package.")
    r = requests.get(url, allow_redirects=True)
    os.chdir(".scratch-modules")
    if verbose:
        print("INFO || Installing package.")
    open(package+'.js', 'wb').write(r.content)
    if verbose:
        print("INFO || Finished!")

def start_server():
    if verbose:
        print("INFO || Starting server.")
    app.run(host="0.0.0.0", port=8000)

# Main

if args.cmd == "init":
    init()
if args.cmd == "update":
    update_repo()
if args.cmd == "install":
    get_package(args.extra)
if args.cmd == "start":
    start_server()
