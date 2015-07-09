#!/usr/bin/env python

"""Uses 'psutil' to gather stats on a system's swap memory usage"""

from __future__ import division # lets us do "real" division
import os
import statsd # this is python-statsd, not the default StatsD library
import sys

try:
	import psutil
except ImportError:
	print "Cannot import 'psutil' - check that it's installed."
	print "Exiting..."
	sys.exit()

STATSD_URL = 'statsd.myserver.com' # or whatever destination
STATSD_PORT = 8125 # just as an example

p = psutil
swap = p.swap_memory()

used = swap.total - swap.free

a1 = int(used / 1024 / 1024)
a2 = int(swap.total / 1024 / 1024)

swap_percentage = (a1 / a2) * 100

def get_swap_stats(): # gather swap memory stats
	print "Swap Usage: %sM / %sM" % (a1, a2)
	print "Usage: %s%%" % swap_percentage

def send_swap_stats(): # sends swap stats to StatsD/Graphite
	GAUGE_NODE = 'noc.server_stats.test_machine.mem_swap'

	statsd_connection = statsd.Connection(host=STATSD_URL, port=STATSD_PORT, sample_rate=1)
	gauge = statsd.Gauge(GAUGE_NODE, statsd_connection)
	gauge.send('count', swap_percentage)

if __name__ == '__main__':
	get_swap_stats()
	send_swap_stats()


"""Something to experiment with later
def bytes2human(n):
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '%.1f%s' % (value, s)
	return "%sB" % n

def pprint_ntuple(nt):
	for name in nt._fields:
		value = getattr(nt, name)
		if name != 'percent':
			value = bytes2human(value)
		print('%-10s: %7s' % (name.capitalize(), value))

def main():
	print('MEMORY\n------')
	pprint_ntuple(psutil.virtual_memory())
	print('\nSWAP\n------')
	pprint_ntuple(psutil.swap_memory())

if __name__ == '__main__':
	main()
"""
