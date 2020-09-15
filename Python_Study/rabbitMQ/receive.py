#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
import pika
from time import sleep
from pika import BasicProperties

connection = pika.BlockingConnection(pika.ConnectionParameters( '10.10.1.81' ))
channel = connection.channel()
data = {'x-max-priority': 20}
channel.queue_declare(queue='hello', arguments=data)
channel.basic_qos(prefetch_count=1)
print('[*] Waiting for messages. To exit press CTRL+C')

da = b''
def callback(ch, method, properties, body):
    da = body
    print(da)
    # sleep(10)

channel.basic_consume(callback, queue='hello', no_ack=True)
channel.start_consuming()
