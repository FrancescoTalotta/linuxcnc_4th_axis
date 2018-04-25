#!/usr/bin/python
from __future__ import print_function

__author__ = 'francesco'

import sys, os

BASE = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
sys.path.insert(0, os.path.join(BASE, "lib", "python"))

import re

passthrough = []

replace = []


def progress(a, b):
    if os.environ.has_key("AXIS_PROGRESS_BAR"):
        print >> sys.stderr, "FILTER_PROGRESS=%d" % int(a * 100. / b + .5)
        sys.stderr.flush()


def main():
    global feedrate, feedrat
    feedrate  = 0
    feedrate2 = 0
    is_on     = True
    infile = sys.argv[1]
    f = open(infile, "r")
    for line in f:
        match = re.match("T(\d\d)(.*)M(\d.*)", line)
        if match:
            tool = int(match.group(1))
            print("M101 P%d" % tool)
            print("T%d M6" % tool)
            print("O100 call [%d]" % tool)
        else:
           print(line.replace("\r", "").replace("\n", ""))

        match = re.match("(.*)STOCK RADIUS=(\d[.]\d\d)(.*)", line)
        if match:
           radius = float(match.group(2))

        match = re.match("(.*)G21(.*)", line)
        if match:
           #print("G21")
           print("O100 sub")
           print("  G49")
           print("  G54")
           print("  #<probe_height> =", radius)
           print("  G0 Z40")
           print("  (MSG,Insert Z Probe, then press S)")
           print("  M0")
           print("  G38.2 Z-30 F140")
           print("  G10 L10 P#1 Z[#<probe_height>]")
           print("  G0 Z40")
           print("  G43")
           print("  (MSG,Remove Z Probe, then press S)")
           print("  M0")
           print("O100 endsub")
           print("(MSG, Set the machine to the tool probe position. If already set click press S to resume. If not set press ESC and set the machine to the desireded tool probe position, then run the program again.)")
           print("M0")
           print("G28.1")
           print("M102")

        match = re.match("S(\d*)(.*)M3", line)
        if (match and is_on):
            speed = int(match.group(1))
            secs  = speed/1200
            print("G4 P%d" % secs)
            is_on = False
	  
        match = re.match("M5(.*)", line)
        if match:
            is_on= True

if __name__ == '__main__':
    main()

# vim:sw=4:sts=4:et:
