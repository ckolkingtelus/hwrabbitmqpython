#!/usr/bin/env python
import pika

# establish a connection with RabbitMQ server.
# broker on the local machine - hence the localhost. If we wanted to connect to a broker on a different machine we'd simply specify its name or IP address here.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# make sure the recipient queue exists. Creating a queue using queue_declare is idempotent ‒ we can run the command as many times as we like, and only one will be created; we're not yet sure which program was run first (send.py or receive.py), so in such cases it's a good practice to repeat declaring the queue in both programs
channel.queue_declare(queue='hello')
