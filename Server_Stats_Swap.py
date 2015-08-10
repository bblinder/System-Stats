#!/usr/bin/env python

from __future__ import division
import os
import statsd # this is python-statsd
import sys

try:
	import psutil
except ImportError:
	print "Cannot import 'psutil' - check that it's installed."
	print "Exiting..."
	sys.exit()


STATSD_URL = 'statsd.myserver.com'
STATSD_PORT = 8125

p = psutil
swap = p.swap_memory()

used = swap.total - swap.free

a1 = int(used / 1024 / 1024)
a2 = int(swap.total / 1024 / 1024)

swap_percentage = (a1 / a2) * 100

def get_swap_stats():
	print "Swap Usage: %sM / %sM" % (a1, a2)
	print "Usage: %s%%" % swap_percentage

def send_swap_stats():
	GAUGE_NODE = 'noc.server_stats.test_machine.mem_swap'

	statsd_connection = statsd.Connection(host=STATSD_URL, port=STATSD_PORT, sample_rate=1)
	gauge = statsd.Gauge(GAUGE_NODE, statsd_connection)
	gauge.send('count', swap_percentage)

if __name__ == '__main__':
	get_swap_stats()
	send_swap_stats()

