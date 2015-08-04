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

STATSD_URL = 'statsd.livestream.com'
STATSD_PORT = 8125

# gathering disk usage stats
p = psutil
usage = p.disk_usage('/')

used = usage.total - usage.free
a1 = int(used / 1024 / 1024 / 1024)
a2 = int(usage.total / 1024 / 1024 / 1024)

print "Disk Usage: %sGB / %sGB" % (a1, a2)

def send_disk_stats_used(): # pushing used disk stats (in GB) to StatsD/Graphite
	disk_used = a1
	
	GAUGE_NODE = 'noc.server_stats.test_machine.disk_usage_used'

	statsd_connection = statsd.Connection(host=STATSD_URL, port=STATSD_PORT, sample_rate=1)
	gauge = statsd.Gauge(GAUGE_NODE, statsd_connection)
	gauge.send('count', disk_used)

def send_disk_stats_total(): # total disk space (in GB)
	disk_total = a2

	GAUGE_NODE = 'noc.server_stats.test_machine.disk_usage_total'
	
	statsd_connection = statsd.Connection(host=STATSD_URL, port=STATSD_PORT, sample_rate=1)
	gauge = statsd.Gauge(GAUGE_NODE, statsd_connection)
	gauge.send('count', disk_total)


if __name__ == '__main__':
	send_disk_stats_used()
	send_disk_stats_total()

