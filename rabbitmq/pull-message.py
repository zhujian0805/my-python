#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials(sys.argv[1], sys.argv[2])
connection = pika.BlockingConnection(pika.ConnectionParameters(sys.argv[3], 5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='BIAPI',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[4:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='BIAPI',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_qos(prefetch_count=1000)
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
