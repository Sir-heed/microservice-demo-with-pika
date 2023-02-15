import pika, json

params = pika.URLParameters('amqps://oaeemxzt:ypx7KJTbXr0aPkyoZu-rj62sk7ju9k4B@moose.rmq.cloudamqp.com/oaeemxzt')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    # channel.basic_publish(exchange='', routing_key='main', body='hello', properties=properties)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)