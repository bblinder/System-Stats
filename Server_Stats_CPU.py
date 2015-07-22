#!/usr/bin/env python

import statsd # this is python-statsd, NOT the default statsd library
import os
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
CPU_count_physical = p.cpu_count(logical=False) # reports physical CPU count.
CPU_count_logical = p.cpu_count() # reports logical CPU count.

percs = p.cpu_percent(interval=1, percpu=True)

print "Number of CPUs (physical): %s" % CPU_count_physical
print "Number of CPUs (logical): %s"'\n' % CPU_count_logical

def cpu_stats_total():
	# set 'percpu=True' to see individual CPU usage
	CPU_percentage = p.cpu_percent(interval=1, percpu=False)
	
	print "CPU Percentage (total) : %s%%" % CPU_percentage

	# Pushing CPU stats to Graphite
	GAUGE_NODE = 'noc.server_stats.test_machine.cpu'

	statsd_connection = statsd.Connection(host=STATSD_URL, port=STATSD_PORT, sample_rate=1)
	gauge = statsd.Gauge(GAUGE_NODE, statsd_connection)
	gauge.send('count', CPU_percentage)


def cpu_stats_individual():
	# prints 'top' style output of each individual CPU/core and adds them to a dict.
	iCpu = 1
	cpus={}
	for perc in percs:
		cpus['CPU' + str(iCpu)] = perc
		iCpu+=1

	CPU1 = cpus['CPU1']
	CPU2 = cpus['CPU2']
	CPU3 = cpus['CPU3']
	CPU4 = cpus['CPU4']
	CPU5 = cpus['CPU5']
	CPU6 = cpus['CPU6']
	CPU7 = cpus['CPU7']
	CPU8 = cpus['CPU8']

	# There's probably a quicker way to list these...
	GAUGE_NODE_CPU1 = 'noc.server_stats.test_machine.cpu1'
	GAUGE_NODE_CPU2 = 'noc.server_stats.test_machine.cpu2'
	GAUGE_NODE_CPU3 = 'noc.server_stats.test_machine.cpu3'
	GAUGE_NODE_CPU4 = 'noc.server_stats.test_machine.cpu4'
	GAUGE_NODE_CPU5 = 'noc.server_stats.test_machine.cpu5'
	GAUGE_NODE_CPU6 = 'noc.server_stats.test_machine.cpu6'
	GAUGE_NODE_CPU7 = 'noc.server_stats.test_machine.cpu7'
	GAUGE_NODE_CPU8 = 'noc.server_stats.test_machine.cpu8'

	# pushing CPU stats, one at a time.

	statsd_connection = statsd.Connection(host=STATSD_URL, port=STATSD_PORT, sample_rate=1)

	#CPU 1
	print "CPU 1: %s%%" % CPU1
	gauge_cpu1 = statsd.Gauge(GAUGE_NODE_CPU1, statsd_connection)
	gauge_cpu1.send('count', CPU1)

	#CPU 2
	print "CPU 2: %s%%" % CPU2
	gauge_cpu2 = statsd.Gauge(GAUGE_NODE_CPU2, statsd_connection)
	gauge_cpu2.send('count', CPU2)

	#CPU 3
	print "CPU 3: %s%%" % CPU3
	gauge_cpu3 = statsd.Gauge(GAUGE_NODE_CPU3, statsd_connection)
	gauge_cpu3.send('count', CPU3)

	#CPU 4
	print "CPU 4: %s%%" % CPU4
	gauge_cpu4 = statsd.Gauge(GAUGE_NODE_CPU4, statsd_connection)
	gauge_cpu4.send('count', CPU4)

	#CPU 5
	print "CPU 5: %s%%" % CPU5
	gauge_cpu5 = statsd.Gauge(GAUGE_NODE_CPU5, statsd_connection)
	gauge_cpu5.send('count', CPU5)

	#CPU 6
	print "CPU 6: %s%%" % CPU6
	gauge_cpu6 = statsd.Gauge(GAUGE_NODE_CPU6, statsd_connection)
	gauge_cpu6.send('count', CPU6)

	#CPU 7
	print "CPU 7: %s%%" % CPU7
	gauge_cpu7 = statsd.Gauge(GAUGE_NODE_CPU7, statsd_connection)
	gauge_cpu7.send('count', CPU7)

	#CPU 8
	print "CPU 8: %s%%" % CPU8
	gauge_cpu8 = statsd.Gauge(GAUGE_NODE_CPU8, statsd_connection)
	gauge_cpu8.send('count', CPU8)


if __name__ == '__main__':
	cpu_stats_total()
	cpu_stats_individual()

