#!/usr/bin/env python
"""Tick-Tock! RCD1610 Ethernet relay board controller.

This small tool can help you to control the relay board and
monitor its current status.
                                    PHLin <po-hsu.lin@canonical.com>
"""

import sys
import json
import time
import urllib2
import argparse

IP = "http://192.168.1.25"
API = "/pwr/relays/"
ACTION = "&value="
PASSWD = "123456"
RELAYS = 16
TIMEOUT = 1


class colors:

    """ANSI color code."""

    g = "\033[32m"
    r = "\033[31m"
    y = "\033[33m"
    end = "\033[m"


STAT = [colors.r + "OFF" + colors.end,
        colors.g + " ON" + colors.end]


def _print_relay():
    """Print the relay number sequentially."""
    print "Query with timeout={} seconds on each relay".format(TIMEOUT)
    output = "Relay:"
    for i in range(1, RELAYS + 1, 1):
        output += ("%2i |" % i)
    print output


def _print_status():
    """Print the relay status sequentially."""
    err_flag = False
    output = "Stat: "
    for i in range(1, RELAYS + 1, 1):
        try:
            url = IP + API + '{}?ac={}'.format(i, PASSWD)
            response = json.loads(urllib2.urlopen(url, timeout=TIMEOUT).read())['v']
            output += STAT[response] + "|"
        except urllib2.URLError, e:
            err_flag = True
            output += (colors.y + "ERR" + colors.end + "|")
            sys.stdout.write("\r%s" % output)
        except KeyboardInterrupt:
            sys.exit(0)
    sys.stdout.write("\r%s" % output)
    if err_flag:
        print("\nError: " + str(e.reason))
        sys.exit(1)


def status():
    """Print both the relay number and their status."""
    _print_relay()
    _print_status()
    print("")


def monitor(rate):
    """Live update for the relay status."""
    print("Ctrl + C to exit (update in %i seconds)" % rate)
    _print_relay()
    while True:
        try:
            _print_status()
            sys.stdout.flush()
            time.sleep(rate)
        except KeyboardInterrupt:
            print("")
            break


def activate(targets):
    """Invert the status of the assigned relay."""
    for i in targets:
        if i < 1 or i > RELAYS:
            print("ERR: Relay number %i out of range, skipping" % i)
            continue
        url = IP + API + "{}?ac={}".format(i, PASSWD)
        try:
            response = 1 - json.loads(urllib2.urlopen(url).read())['v']
            url = IP + API + "{}?ac={}".format(i, PASSWD) + ACTION + str(response)
            response = json.loads(urllib2.urlopen(url).read())['v']
            print("Relay %i is now in %s stat" % (i, STAT[response]))
        except urllib2.URLError, e:
            print("Error: " + str(e.reason))
            break


def main():
    """Argument parser and major tasks here."""
    parser = argparse.ArgumentParser(description="Ethernet relay board toybox")
    subparsers = parser.add_subparsers(dest='subparser_name')
    monitor_parser = subparsers.add_parser('monitor',
                                           help="Keep watching relay status")
    monitor_parser.set_defaults(func=monitor)
    monitor_parser.add_argument('-r', '--refresh',
                                dest='idx',
                                metavar='T',
                                default=2,
                                type=int,
                                help="Refresh rate (T seconds)")
    stat_parser = subparsers.add_parser('status',
                                        help="Query the status of all relays")
    stat_parser.set_defaults(func=status)
    flip_parser = subparsers.add_parser('flip',
                                        help="Invert the status of certain relay(s)")
    flip_parser.set_defaults(func=activate)
    flip_parser.add_argument('idx',
                             default=[],
                             nargs='*',
                             type=int,
                             help="The index of relay(s)")
    args = parser.parse_args()

    if args.func.func_name is None:
        parser.parse_args(['-h'])
    else:
        if args.func.func_name is not 'status':
            args.func(args.idx)
        else:
            args.func()


if __name__ == "__main__":
    main()
