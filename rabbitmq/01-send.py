#!/usr/bin/env python
import pika
import sys
from pika import credentials as pika_credentials

conn_parameters = pika.ConnectionParameters(host=sys.argv[1], port=int(sys.argv[2]), credentials=pika_credentials.PlainCredentials(sys.argv[3], sys.argv[4]))

connection = pika.BlockingConnection(conn_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='testing.001', type='topic', durable=True, auto_delete=False)

#channel.queue_declare(queue='testing', durable=True)

channel.basic_publish(exchange=sys.argv[5], routing_key=sys.argv[6], body=sys.argv[7], properties=pika.BasicProperties(delivery_mode = 2,))

print " [x] Sent %s " % sys.argv[7]

connection.close()
