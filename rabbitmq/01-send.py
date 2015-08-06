#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters( host='ip'))

channel = connection.channel()

channel.exchange_declare(exchange='testing.001', type='topic', durable=True, auto_delete=False)

#channel.queue_declare(queue='testing', durable=True)

channel.basic_publish(exchange=sys.argv[1], routing_key=sys.argv[2], body=sys.argv[3], properties=pika.BasicProperties(delivery_mode = 2,))

print " [x] Sent %s " % sys.argv[3]

connection.close()
