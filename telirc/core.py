# -*- coding: utf-8 -*-
# This software is distributed under the two-clause BSD license.

"""Core dispatcher."""

import asyncio

class Core(object):
    def __init__(self, listeners, relay):
        self.listeners = listeners
        self.relay = relay
        self.queue = asyncio.Queue()

    @asyncio.coroutine
    def connect_all(self):
        for listener in self.listeners:
            listener.set_queue(self.queue)

        connectors = [
            obj.connect()
            for obj in [self.relay] + self.listeners
        ]
        done, pending = yield from asyncio.wait(connectors)
        if pending:
            raise Exception("Kaboom!!")

    @asyncio.coroutine
    def run(self):
        while True:
            yield from self.connect_all()
            print("Connected.")

            while True:
                message = yield from self.queue.get()
                yield from self.relay.send(message)

    def __repr__(self):
        return '<Core(%r, %r)>' % (self.listeners, self.relay)
