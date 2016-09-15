#!/usr/bin/python
import math
import matplotlib.pyplot as plt
import numpy as np
import argparse
from sys import argv

import struct
record_len = 4
records = 0
data = [[],[]]
clock = []
errorx = []
errors = []
start_point = 0


parser = argparse.ArgumentParser(description="visualise and test data")
parser.add_argument('--file', action='store',
    default='raw', help="data file to load, otherwise uses stdin")
parser.add_argument('--max', action='store', type=int,
    help="max records to parse")
parser.add_argument('--skip', action='store', type=int, default=1,
    help="only process 1 in skip records")
parser.add_argument('--test-count', help='check data integrity',
    action="store", type=int, dest="wrap")
parser.add_argument('--dump', help='dump data to file', action="store_const",
    const=True)
parser.add_argument('--plot', help='plot', action="store_const",
    const=True)
parser.add_argument('--channels', help='0,1 or both', action="store", default='0')

args = parser.parse_args()
record_len = 4
try:
    with open(args.file, 'r') as fh:
        record = fh.read(record_len)
        # skip first record
        record = fh.read(record_len)
        while record != "":
            chan1, chan2 = struct.unpack("HH", record)

            if records == 0:
                start_point = chan1

            if args.channels == '0' or args.channels == 'both':
                data[0].append(chan1)
            if args.channels == '1' or args.channels == 'both':
                data[1].append(chan2)

            if args.wrap:
                clock.append((records + start_point)% args.wrap)
                if chan1 - ((records + start_point) %args.wrap):
                    errorx.append(records)
                    errors.append(chan1)
            if records % 100000 == 0:
                    print("processed %d records with %d errors" % (records, len(errors)))
            if args.max and records > args.max:
                break;
                
            records += 1

            if args.skip:
                fh.seek(args.skip * record_len - record_len, 1)

            record = fh.read(record_len)

except KeyboardInterrupt:
    pass

print("processed %d records with %d errors" % (records, len(errors)))

if args.dump:
    with open("processed", 'w') as fh:
        for d0, d1 in zip(data[0], data[1]):
            fh.write("%d,%d\n" % (d0, d1))
        print("wrote %d records" % records)


if args.plot:

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    if args.channels == '0' or args.channels == 'both':
        x = range(0,len(data[0])*args.skip,args.skip)
        ax.plot(x, data[0], 'g')
    if args.channels == '1' or args.channels == 'both':
        x = range(0,len(data[1])*args.skip,args.skip)
        ax.plot(x, data[1], 'y')

    if args.wrap:
        ax.plot(errorx, errors, 'bs') 
        ax.plot(x, clock, 'r') 


    ax.set_ylim(0,5000)
    plt.xlabel('sample #')
    plt.grid(True)
    plt.title('data integrity')
    plt.show()
