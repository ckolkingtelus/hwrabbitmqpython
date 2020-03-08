#!/usr/bin/env python
# coding: utf-8 
import pika

# NOTE: Production [Non-]Suitability Disclaimer
# NOTE: Please keep in mind that this and other tutorials are, well, tutorials. They demonstrate one new concept at a time and may intentionally oversimplify some things and leave out others. For example topics such as connection management, error handling, connection recovery, concurrency and metric collection are largely omitted for the sake of brevity. Such simplified code should not be considered production ready.

# establish a connection with RabbitMQ server.
# broker on the local machine - hence the localhost. If we wanted to connect to a broker on a different machine we'd simply specify its name or IP address here.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# ISSUE: the character "‒" copied from the webpage is not straight up ASCII, so produces a syntax error when running this python code: "SyntaxError: Non-ASCII character '\xe2' in file send.py on line... but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details"
# FIX: add the line at the top "# coding: utf-8" 
# make sure the recipient queue exists. Creating a queue using queue_declare is idempotent ‒ we can run the command as many times as we like, and only one will be created; we're not yet sure which program was run first (send.py or receive.py), so in such cases it's a good practice to repeat declaring the queue in both programs
channel.queue_declare(queue='hello')

# receiving works by subscribing a callback function to a queue. Whenever we receive a message, this callback function is called by the Pika library. In our case this function will print on the screen the contents of the message.
def callback_for_helloqueue(ch, method, properties, body):
    print(" [x] Received %r" % body)

# tell RabbitMQ that this particular callback function should receive messages from our hello queue:
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback_for_helloqueue)

# finally, we enter a never-ending loop that waits for data and runs callbacks whenever necessary
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
