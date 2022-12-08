#!/usr/bin/env python3
import argparse
#Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument("cmd", help="The command you use")
args = parser.parse_args()
# Main
if args.cmd == "init":
    pass
    