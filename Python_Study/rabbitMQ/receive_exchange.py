#!/usr/bin/env python
#coding=utf-8
import pika
 
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
#定义交换机-广播模式
channel.exchange_declare(exchange='messages', type='fanout')
#随机生成队列，并绑定到交换机上
result = channel.queue_declare(exclusive=True)  # exclusive=True接收端退出时，销毁临时队列
queue_name = result.method.queue
channel.queue_bind(exchange='messages', queue=queue_name)
 
def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
channel.basic_consume(callback, queue=queue_name, no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
