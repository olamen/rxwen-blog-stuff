#!/usr/bin/env python
# -*- coding: utf-8 -*-

__VERSION__ = '1.0.0'
__author__ = 'rx.wen218@gmail.com'

import subprocess
import sys
import shutil
import os
from optparse import OptionParser

SUCCESS = 0

# parse command line options
opt_parser = OptionParser(version = "%prog " + __VERSION__, 
            description = "command line tool for generating cscope database",
            usage = "%prog [-o file] [file type: c/java]")
opt_parser.add_option("-o", "--output", dest="output_file", default="cscope.out", help="cscope database file")
opt_parser.add_option("-i", "--input", dest="input_file", default=".bcscope.cfg", help="cfg file lists all directories to be searched")
opt_parser.add_option("-v", "--verbose", action="store_true", default=False, help="verbose output [default: %default]")
(cmdline_options, args) = opt_parser.parse_args()

# config application behavior
valid_lan_types = {"c++": ".*\.\(cpp\|c\|cxx\|cc\|h\|hpp\|hxx\)",
    "java": ".*\.java"}
lan_type = "c++"
if len(args) > 0:
    lan_type = args[0]
if valid_lan_types.has_key(lan_type):
    lan_pattern = valid_lan_types[lan_type]
else:
    print "invalid language type: " + lan_type
    print "must be one of:"
    for (k, v) in valid_lan_types.items():
        print "\t" + k
    sys.exit(-1)

file_list_name = "cscope.files"
file_list = open(file_list_name, "w")
# should we check more directories?
dirs = []
if os.path.isfile(cmdline_options.input_file):
    f = open(cmdline_options.input_file)
    for line in f:
        line = line.strip() # remove possible \n char
        if len(line) > 0 and not line.startswith("#"):
            line = os.path.expanduser(line)
            dirs.append(line)
# make sure current directory is included
if dirs.count(".") + dirs.count("./") < 1:
    dirs.append(".")

# find source files in all directories
for d in dirs:
    print "find " + lan_type + " source files in " + d
    subprocess.Popen(["find", d, "-regex", lan_pattern], stdout=file_list).wait()
# actually generate database
print "build cscope database"
subprocess.Popen(["cscope", "-b"]).wait()
shutil.move("cscope.out", cmdline_options.output_file)
os.remove(file_list_name)
print "done, cscope database saved in " + cmdline_options.output_file

