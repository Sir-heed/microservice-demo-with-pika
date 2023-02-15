import pika, json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from product.models import Product

params = pika.URLParameters('amqps://oaeemxzt:ypx7KJTbXr0aPkyoZu-rj62sk7ju9k4B@moose.rmq.cloudamqp.com/oaeemxzt')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print("Received in admin")
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product.objects.create(product_id=data['id'], title=data['title'], image=data['image'])
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.objects.get(product_id=data['id'])
        product.title = data['title']
        product.image = data['image']
        product.save()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.objects.get(product_id=product)
        product.delete()
        print('Product Deleted')

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
print("Started Consuming")
channel.start_consuming()
channel.close()