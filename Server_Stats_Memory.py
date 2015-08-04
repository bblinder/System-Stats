#!/usr/bin/env python

from __future__ import division # lets us do "real" division
import datetime
import statsd # this is python-statsd, NOT the default statsd library
import os
import sys

try:
	import psutil
except ImportError:
	print "Cannot import 'psutil' - please check that it's installed"
	print "Exiting..."
	sys.exit()


STATSD_URL = 'statsd.livestream.com'
STATSD_PORT = 8125

def mem_stats():
	p = psutil
	MEM = p.virtual_memory()

	used = MEM.total - MEM.available
	a1 = int(used / 1024 / 1024)
	a2 = int(MEM.total / 1024 / 1024)

	mem_percentage = (a1 / a2) * 100

	print "Used Memory: %sM (%s%%)" % (a1, mem_percentage)
	print "Total Memory: %sM" % a2

	# Pushing memory stats to Graphite
	GAUGE_NODE = 'noc.server_stats.test_machine.mem_used'

	statsd_connection = statsd.Connection(host=STATSD_URL, port=STATSD_PORT, sample_rate=1)
	gauge = statsd.Gauge(GAUGE_NODE, statsd_connection)
	gauge.send('count', mem_percentage)


if __name__ == '__main__':
	mem_stats()

