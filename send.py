#!/usr/bin/env python
# coding: utf-8 
import pika

# NOTE: Production [Non-]Suitability Disclaimer
# NOTE: Please keep in mind that this and other tutorials are, well, tutorials. They demonstrate one new concept at a time and may intentionally oversimplify some things and leave out others. For example topics such as connection management, error handling, connection recovery, concurrency and metric collection are largely omitted for the sake of brevity. Such simplified code should not be considered production ready.

# establish a connection with RabbitMQ server.
# broker on the local machine - hence the localhost. If we wanted to connect to a broker on a different machine we'd simply specify its name or IP address here.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# make sure the recipient queue exists. If we send a message to non-existing location, RabbitMQ will just drop the message. Let's create a hello queue to which the message will be delivered
channel.queue_declare(queue='hello')

# ISSUE: the character "‒" copied from the webpage is not straight up ASCII, so produces a syntax error when running this python code: "SyntaxError: Non-ASCII character '\xe2' in file send.py on line... but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details"
# FIX: add the line at the top "# coding: utf-8" 
# RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange. But let's not get dragged down by the details ‒ you can read more about exchanges in the third part of this tutorial. All we need to know now is how to use a default exchange identified by an empty string. This exchange is special ‒ it allows us to specify exactly to which queue the message should go. The queue name needs to be specified in the routing_key parameter:
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

# Before exiting the program we need to make sure the network buffers were flushed and our message was actually delivered to RabbitMQ. We can do it by gently closing the connection
connection.close()
