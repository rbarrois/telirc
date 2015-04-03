telirc
======

telirc is a simple IRC notifier.
It will forward any messages it receives into a configured network/channel.

Usage
-----

.. code-block:: sh

    # Copy all messages from stdin to chan #fubar on irc.example.org
    telirc irc.example.org#fubar -

    # Copy messages from an udp socket to chan #fubar on irc.example.org,
    # using nick 'telirc' and nickserv pass 'sikrit'
    telirc telirc:sikrit@irc.example.org#fubar udp:127.0.0.1:123

Links
-----

* Source code on GitHub: https://github.com/rbarrois/telirc
* Available on PyPI: https://pypi.python.org/pypi/telirc


Protocol
--------

The format of incoming messages is quite simple: ``v1\0source\0level\0the actual message\n``

In details:

* All text **MUST** be UTF-8 encoded
* Each message **MUST** end with a linefeed (``\n``)
* Messages are composed of 4 fields, separated by a null byte (``\0``):

  - The protocol version
  - An identifier for the emitter
  - The message level (info/warn/crit)
  - The actual message


Requirements
------------

``telirc`` is implemented in Python, and requires at least Python 3.4.
