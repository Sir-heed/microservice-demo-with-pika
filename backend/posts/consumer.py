import pika, json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()
from product.models import Product

params = pika.URLParameters('amqps://oaeemxzt:ypx7KJTbXr0aPkyoZu-rj62sk7ju9k4B@moose.rmq.cloudamqp.com/oaeemxzt')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print("Received in admin")
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_liked':
        product = Product.objects.get(id=data)
        product.likes = product.likes + 1
        product.save()
        print('Product likes increased')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print("Started Consuming")
channel.start_consuming()
channel.close()