#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
import pika  
import sys  
parameters = pika.ConnectionParameters(host = '10.10.1.81' )
connection = pika.BlockingConnection(parameters)  
channel = connection.channel()  
channel.queue_declare(queue = 'task_queue' , durable = True )  
message = ' ' .join(sys.argv[ 1 :]) or "Hello World!"  
channel.basic_publish(exchange = '',  
                        routing_key = 'task_queue' ,  
                        body = message,  
                        properties = pika.BasicProperties(  
                        delivery_mode = 2 , # make message persistent  
                       ))  
print(" [x] Sent %r" % (message,))  
connection.close() 