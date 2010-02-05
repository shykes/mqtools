#!/usr/bin/env python

import sys

import argparse
from carrot.connection import BrokerConnection
from carrot.messaging import Publisher, Consumer

parser = argparse.ArgumentParser(description="Read a text stream and send it to an AMQP broker")
subcommands = parser.add_subparsers(dest="command")

parser_consume = subcommands.add_parser("consume", help="consume amqp messages and write them to stdout")
parser_consume.add_argument("hostname", help="Hostname of the AMQP broker")
parser_consume.add_argument("queue", help="Queue to use on the AMQP broker")
parser_consume.add_argument("--exchange", help="Create a fanout exchange and bind it to the queue", default=None)
parser_consume.add_argument("-u", "--user", help="User for the AMQP broker", default=None)
parser_consume.add_argument("-p", "--password", help="Password for the AMQP broker", default=None)
parser_consume.add_argument("-v", "--vhost", help="Virtual host to use on the AMQP broker", default="/")
parser_consume.add_argument("--ack", help="Acknowledge messages, removing them from the queue", action="store_true")

parser_send = subcommands.add_parser("send", help="Read lines from stdin, send them to an amqp broker")
parser_send.add_argument("hostname", help="Hostname of the AMQP broker")
parser_send.add_argument("exchange", help="Exchange to use on the AMQP broker")
parser_send.add_argument("--key", help="Routing key to use on the AMQP broker")
parser_send.add_argument("-v", "--vhost", help="Virtual host to use on the AMQP broker", default="/")
parser_send.add_argument("-u", "--user", help="User for the AMQP broker", default=None)
parser_send.add_argument("-p", "--password", help="Password for the AMQP broker", default=None)

def main():
    args = parser.parse_args()
    conn = BrokerConnection(
            hostname=args.hostname,
            virtual_host=args.vhost,
            userid=args.user,
            password=args.password,
    )
    if args.command == "consume":
        consumer = Consumer(
                connection      = conn,
                exchange_type   = "fanout" if args.exchange else None,
                exchange        = args.exchange,
                queue           = args.queue
        )
        def display_message(data, msg):
            print str(data)
            if args.ack:
                msg.ack()
        consumer.register_callback(display_message)
        consumer.wait()
    elif args.command == "send":
        publisher = Publisher(
                auto_declare    = False,
                connection      = conn,
                exchange        = args.exchange,
                routing_key     = args.key
        )
        for line in sys.stdin.readlines():
            publisher.send(line.strip())
        publisher.close()
