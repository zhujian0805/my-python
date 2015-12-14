#!/usr/bin/env python
import pika
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters(host='ip'))
channel = connection.channel()

channel.exchange_declare(exchange=sys.argv[1], type='topic', durable=True)

result = channel.queue_declare(exclusive=True, durable=True)

queue_name = result.method.queue

channel.queue_bind(exchange=sys.argv[1], queue=sys.argv[2])

print ' [*] Waiting for logs. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)

channel.basic_consume(callback, queue=sys.argv[2], no_ack=True)

channel.start_consuming()
