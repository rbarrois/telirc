# -*- coding: utf-8 -*-
# This software is distributed under the two-clause BSD license.


import asyncio


DEFAULT_IRC_PORT = 6667


class IRCRelay(object):
    def __init__(self, nick, host, port, channel, nick_pass='', net_pass=''):
        self.nick = nick
        self.host = host
        self.port = port or DEFAULT_IRC_PORT
        self.channel = channel
        self.nick_pass = nick_pass
        self.net_pass = net_pass

    @asyncio.coroutine
    def connect(self):
        print("%r connected" % self)

    @asyncio.coroutine
    def send(self, message):
        pass


class StdoutRelay(object):
    """A fake relay sending to stdout."""

    @asyncio.coroutine
    def connect(self):
        print("%r connected" % self)

    @asyncio.coroutine
    def send(self, message):
        print(message)
