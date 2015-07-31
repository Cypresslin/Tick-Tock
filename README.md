Tick-Tock!
===========
A small command-line tool to control and monitor your ethernet relay board.

It was programmed base on the RCD1610 ethernet relay board, which provides
a WebAPI that use GET method to access the board over HTTP and return the
status in JSON format.

Therefore, it's easy to adapt the code for products from different vendor
you just need to tweak the API entry (and maybe the response code).

## Configuration
For RCD1610 (or RCD series) users, just change the IP address, the number
of relays and the access credential in the code and you're ready:

    IP = "http://192.168.1.25"
    PASSWD = "123456"
    RELAYS = 16

## License
GPLv2

## Why "Tick-Tock!"?
Have you ever heard of the sound of a relay in action? :P
