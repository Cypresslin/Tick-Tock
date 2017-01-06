Tick-Tock!
===========
A small command-line tool to control and monitor your Ethernet relay board.

It was programmed for the tinycdc RCD1610 Ethernet relay board, which
provides a WebAPI that use GET method to access the board over HTTP and
return the status in JSON format.

Therefore, it's easy to adapt the code for products from different vendor
you just need to tweak the API entry (and maybe the response code).

## Configuration
For RCD1610 (or RCD series) users, just change the IP address, the number
of relays and the access credential in the settings.txt and you're ready:

    IP = "http://192.168.1.25"
    PASSWD = "123456"
    RELAYS = 16

For more advanced operation, you can change the API and ACTION variable.

## Usage
To flip (multiple) relay status in-between ON and OFF:

    $ python3 ./tick-tock.py flip 1 2
    Relay  1 is now in  ON stat
    Relay  2 is now in  ON stat

To monitor the relay status in every 5 seconds

    $ python3 ./tick-tock.py monitor
    Ctrl + C to exit (update in 5 seconds)
    Query with timeout = 1 seconds on each relay
    Relay: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |10 |11 |12 |13 |14 |15 |16 |
    Stat:  ON| ON|OFF|OFF|OFF|OFF|OFF|OFF| ON|OFF|OFF|OFF|OFF|OFF|OFF|OFF|

## License
GPLv2

## Why "Tick-Tock!"?
Have you ever heard of the sound of a relay in action? :P
