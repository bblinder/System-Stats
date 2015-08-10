#!/usr/bin/env python

from __future__ import division # lets us do some "real" division
import statsd # this is python-statsd, NOT the default statsd library
import os
import sys

try:
	import psutil
except ImportError:
	print "Cannot import 'psutil' - please check that it's installed"
	print "Exiting..."
	sys.exit()

STATSD_URL = 'statsd.myserver.com'
STATSD_PORT = 8125

def disk_usage(): # gathering disk usage stats
	p = psutil
	usage = p.disk_usage('/')
	
	used = usage.total - usage.free
	a1 = int(used / 1024 / 1024 / 1024)
	a2 = int(usage.total / 1024 / 1024 / 1024)
	
	disk_percentage = (a1 / a2) * 100

	print "Disk Usage: %sGB / %sGB" % (a1, a2)
	print "Percent Full: %s%%" % disk_percentage
	
	return disk_percentage

def send_disk_stats(): # pushing disk usage stats to StatsD/Graphite
	disk_percentage = disk_usage()

	GAUGE_NODE = 'noc.server_stats.test_machine.disk_usage'

	statsd_connection = statsd.Connection(host=STATSD_URL, port=STATSD_PORT, sample_rate=1)
	gauge = statsd.Gauge(GAUGE_NODE, statsd_connection)
	gauge.send('count', disk_percentage)


if __name__ == '__main__':
	disk_usage()
	send_disk_stats()

