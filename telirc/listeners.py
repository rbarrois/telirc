# -*- coding: utf-8 -*-
# This software is distributed under the two-clause BSD license.

import asyncio
import concurrent
import functools
import logging

logger = logging.getLogger(__name__)


class BaseListener(object):
    def __init__(self):
        self.queue = None

    def set_queue(self, queue):
        self.queue = queue

    @asyncio.coroutine
    def connect(self):
        print("%r connected" % self)

    @asyncio.coroutine
    def get_message(self):
        yield 42


class StdinListener(BaseListener):
    def __repr__(self):
        return 'StdinListener()'


class SocketListener(BaseListener):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def __repr__(self):
        return 'SocketListener(%r)' % self.path


class _UDPProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue, name, **kwargs):
        super().__init__(**kwargs)
        self.queue = queue
        self.transport = None
        self.name = name

    def _info(self, msg, *args):
        logger.info("%s: " + msg, self.name, *args)

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        self._info("Received data from %s:%s", addr[0], addr[1])
        self.queue.put(data)

    def connection_lost(self, exc):
        self._info("Lost connection: %r", exc)


class UDPListener(BaseListener):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.transport = None
        self.protocol = None

    def _info(self, msg, *args):
        logger.info("UDP[%s:%d]: " + msg, self.host, self.port, *args)

    @asyncio.coroutine
    def connect(self):
        loop = asyncio.get_event_loop()
        self.transport, self.protocol = yield from loop.create_datagram_endpoint(
            functools.partial(_UDPProtocol, self.queue, 'UDP[%s:%d]' % (self.host, self.port)),
            local_addr=(self.host, self.port))
        print("%r: connected" % self)

    def __repr__(self):
        return 'UDPListener(%r, %r)' % (self.host, self.port)


class TCPListener(BaseListener):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server = None

    def _info(self, msg, *args):
        logger.info("TCP[%s:%d]: " + msg, self.host, self.port, *args)

    @asyncio.coroutine
    def add_client(self, reader, writer):
        self._info("client connected")
        while not reader.at_eof():
            msg = yield from reader.readline()
            if msg:
                yield from self.queue.put(msg)
            else:
                self._info("client lost")
                reader.feed_eof()

    @asyncio.coroutine
    def connect(self):
        self.server = yield from asyncio.start_server(self.add_client, self.host, self.port)

    def __repr__(self):
        return 'TCPListener(%r, %r)' % (self.host, self.port)
