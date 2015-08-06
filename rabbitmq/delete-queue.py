#!/usr/bin/python
"""
Issue:
-------
We use RabbitMQ as part of our alert processing backend for our server monitoring service,
Server Density. Earlier this week we had a problem with one of our queues suddenly getting
very large which caused RabbitMQ to exceed its memory limit. When this happened it
prevented RabbitMQ from accepting any new connections.

Solution 1:
----------
See the following code

Solution 2:
----------
Removing the data files
Without any method to delete the queue, the only alternative is to stop RabbitMQ, remove
the data files and then restart it. We are using durable queues so restarting the server
without removing the data files would make no difference. This was a case of moving the
files from /var/lib/rabbitmq/mnesia/rabbit@rabbit1 elsewhere so that RabbitMQ could not
find them. This resolved the problem.
"""
import pika

host = 'rabbitmq1'
creds = pika.PlainCredentials('username', 'password')
params = pika.ConnectionParameters(host, credentials=creds)
conn = pika.AsyncoreConnection(params)
ch = conn.channel()
ch.queue_delete(queue='queuename')
ch.close()
conn.close()
