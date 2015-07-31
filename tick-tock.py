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
    output = "Relay:"
    for i in range(1, RELAYS + 1, 1):
        output += ("%2i |" % i)
    print output


def _print_status():
    """Print the relay status sequentially."""
    output = "Stat: "
    for i in range(1, RELAYS + 1, 1):
        try:
            url = IP + API + '{}?ac={}'.format(i, PASSWD)
            response = json.loads(urllib2.urlopen(url).read())['v']
            output += STAT[response] + "|"
        except:
            output += (colors.y + "ERR" + colors.end + "|")
    sys.stdout.write("\r%s" % output)


def status():
    """Print both the relay number and their status."""
    _print_relay()
    _print_status()
    print("")


def monitor():
    """Live update for the relay status."""
    print("Ctrl + C to exit (update in 2 seconds)")
    _print_relay()
    while True:
        try:
            _print_status()
            sys.stdout.flush()
            time.sleep(1)
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
        response = 1 - json.loads(urllib2.urlopen(url).read())['v']
        url = IP + API + "{}?ac={}".format(i, PASSWD) + ACTION + str(response)
        response = json.loads(urllib2.urlopen(url).read())['v']
        print("Relay %i is now in %s stat" % (i, STAT[response]))


def main():
    """Argument parser and major tasks here."""
    parser = argparse.ArgumentParser(description="Ethernet relay board toybox")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('targets',
                       default=[],
                       action='store',
                       type=int,
                       nargs='*',
                       help="Flip the status of relay #")
    group.add_argument('-s', '--status',
                       dest='cmd',
                       action='store_const',
                       const=status,
                       help="Query relay status")
    group.add_argument('-m', '--monitor',
                       dest='cmd',
                       action='store_const',
                       const=monitor,
                       help="Keep watching relay status")
    args = parser.parse_args()
    if args.cmd is None and not args.targets:
        parser.parse_args(['-h'])
    else:
        if not args.targets:
            args.cmd()
        else:
            activate(args.targets)


if __name__ == "__main__":
    main()
