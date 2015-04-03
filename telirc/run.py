# -*- coding: utf-8 -*-
# This software is distributed under the two-clause BSD license.

import asyncio
import re

from . import core
from . import listeners
from . import relays


def build_listener(name):
    if name == '-':
        return listeners.StdinListener()
    elif name.startswith('socket:'):
        return listeners.SocketListener(name[len('socket:'):])
    elif name.startswith('udp:') and name.count(':') == 2:
        _proto, host, port = name.split(':')
        port = int(port)
        return listeners.UDPListener(host, port)
    elif name.startswith('tcp:') and name.count(':') == 2:
        _proto, host, port = name.split(':')
        port = int(port)
        return listeners.TCPListener(host, port)
    else:
        raise ValueError("Invalid listener format %r" % name)


def build_relay(config):
    match = re.match(r'^(.*)@([\w.-]+)(:\d+)?#(.*)$', config.channel)
    if not match:
        raise ValueError("Invalid channel name %r" % config.channel)

    if config.send_to_stdout:
        return relays.StdoutRelay()
    else:
        nick, server, port, channel = match.groups()
        return relays.IRCRelay(
            nick=nick,
            host=server,
            port=port,
            channel=channel,
            nick_pass=config.nickserv_pass,
        )


def prepare(config):
    sources = [
        build_listener(source)
        for source in config.source
    ]
    relay = build_relay(config)
    return core.Core(
        listeners=sources,
        relay=relay,
    )


def run_forever(config):
    loop = asyncio.get_event_loop()

    telirc_core = prepare(config)
    print(telirc_core)
    loop.run_until_complete(telirc_core.run())

