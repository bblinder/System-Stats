#!/usr/bin/env python

"""
List number of running process IDs
"""
import os
import statsd
import sys

STATSD_URL = 'statsd.livestream.com'
STATSD_PORT = 8125

def process_list():
	pids = []
	for subdir in os.listdir('/proc'):
		if subdir.isdigit():
			pids.append(subdir)

	return pids

pids = process_list()
num_pids = format(len(pids))
print 'Total number of running processes: %s' % num_pids

def send_pids():
	GAUGE_NODE = 'noc.server_stats.test_machine.num_pids'

	statsd_connection = statsd.Connection(host=STATSD_URL, port=STATSD_PORT, sample_rate=1)
	gauge = statsd.Gauge(GAUGE_NODE, statsd_connection)
	gauge.send('count', int(num_pids))

if __name__=='__main__':
	process_list()
	send_pids()

