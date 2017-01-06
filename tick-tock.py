#!/usr/bin/env python3
"""Tick-Tock! RCD1610 Ethernet relay board controller.

This small tool can help you to control the relay board and
monitor its current status.
                                    PHLin <po-hsu.lin@canonical.com>
"""

import argparse
import configparser
import json
import sys
import time
from urllib.request import urlopen, URLError


class colors:

    """ANSI color code."""

    g = "\033[32m"
    r = "\033[31m"
    y = "\033[33m"
    end = "\033[m"


STAT = [colors.r + "OFF" + colors.end,
        colors.g + " ON" + colors.end]


def _load_config():
    """Load the config file."""
    config = configparser.SafeConfigParser()
    config.readfp(open(r'settings.txt'))
    global IP
    global API
    global ACTION
    global PASSWD
    global RELAYS
    global TIMEOUT
    IP = config.get("HW Settings", "IP").replace('"', '')
    API = config.get("HW Settings", "API").replace('"', '')
    ACTION = config.get("HW Settings", "ACTION").replace('"', '')
    PASSWD = config.get("HW Settings", "PASSWD").replace('"', '')
    RELAYS = int(config.get("HW Settings", "RELAYS"))
    TIMEOUT = int(config.get("HW Settings", "TIMEOUT"))


def _print_relay():
    """Print the relay number sequentially."""
    print("Query with timeout = {} seconds on each relay".format(TIMEOUT))
    output = "Relay:"
    for i in range(1, RELAYS + 1, 1):
        output += ("%2i |" % i)
    print(output)


def _print_status():
    """Print the relay status sequentially."""
    err_flag = False
    output = "Stat: "
    for i in range(1, RELAYS + 1, 1):
        try:
            url = IP + API + '{}?ac={}'.format(i, PASSWD)
            response = json.loads(urlopen(url, timeout=TIMEOUT).read().decode("utf-8"))['v']
            output += STAT[response] + "|"
        except URLError as e:
            err_flag = True
            output += (colors.y + "ERR" + colors.end + "|")
            sys.stdout.write("\r%s" % output)
        except KeyboardInterrupt:
            sys.exit(0)
    sys.stdout.write("\r%s" % output)
    if err_flag:
        print("\nERR: " + str(e.reason))
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
    if targets == []:
        print("ERR: please assign relay id(s)")
        sys.exit(1)
    for i in targets:
        if i < 1 or i > RELAYS:
            print("ERR: Relay number %i out of range, skipping" % i)
            continue
        url = IP + API + "{}?ac={}".format(i, PASSWD)
        try:
            response = 1 - json.loads(urlopen(url).read().decode("utf-8"))['v']
            url = IP + API + "{}?ac={}".format(i, PASSWD) + ACTION + str(response)
            response = json.loads(urlopen(url).read().decode("utf-8"))['v']
            print("Relay %i is now in %s stat" % (i, STAT[response]))
        except URLError as e:
            print("ERR: " + str(e.reason))
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
                                        help="Invert the status of given relay(s)")
    flip_parser.set_defaults(func=activate)
    flip_parser.add_argument('idx',
                             default=[],
                             nargs='*',
                             type=int,
                             help="The index of relay(s)")
    args = parser.parse_args()

    if args.func.__name__ is None:
        parser.parse_args(['-h'])
    else:
        _load_config()
        if args.func.__name__ is not 'status':
            args.func(args.idx)
        else:
            args.func()


if __name__ == "__main__":
    main()
