# -*- coding: utf-8 -*-
# This software is distributed under the two-clause BSD license.


import argparse
import logging


from . import run

src_help = """
Sources:
--------

Messages can be received from various sources:

- '-' for standard input
- 'socket:/path/to/socket' for a socket
- 'udp:host:port' for UDP messages listening (use '*' as host for a wildcard listen)
- 'tcp:host:port' for TCP messages listening (use '*' as host for a wildcard listen) 
"""


def make_parser():
    parser = argparse.ArgumentParser(
        description="A simple IRC notifier",
        epilog=src_help,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('channel',
        help="Target channel (format: user@server[:port]#channel)")
    parser.add_argument('source', nargs='+',
        help="Message source ('-', 'socket:/path', 'udp:host:port', 'tcp:host:port')")
    parser.add_argument('--reconnect-delay', type=int,
        help="Delay between reconnect attempts, in seconds (default: 10)")
    parser.add_argument('--nickserv-pass', help="Nickserv password")
    parser.add_argument('--send-to-stdout', action='store_true',
        help="Write messages to stdout instead of IRC")

    return parser


def setup_logging(config):
    lg = logging.getLogger()
    lg.setLevel(logging.INFO)
    lg.addHandler(logging.StreamHandler())


def main(argv):
    parser = make_parser()
    args = parser.parse_args(argv)
    setup_logging(args)
    run.run_forever(args)
