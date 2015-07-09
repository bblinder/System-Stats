#!/usr/bin/env python

from __future__ import division
import psutil
import os
import sys

p = psutil
usage = p.disk_usage('/')

used = usage.total - usage.free
a1 = int(used / 1024 / 1024 / 1024)
a2 = int(usage.total / 1024 / 1024 / 1024)

disk_percentage = (a1 / a2) * 100

print "Disk Usage: %sGB / %sGB" % (a1, a2)
print "Percent Full: %s%%" % disk_percentage

