#!/usr/bin/env python

import os
import re
import subprocess
import sys

def proc_output():
	awk_sort = subprocess.Popen("cat /proc/interrupts | awk 'NR==2','NR==23'", stdout=subprocess.PIPE,\
			shell=True).communicate()[0]
	return awk_sort


if __name__ == '__main__':
	interrupts = proc_output()
	print interrupts

