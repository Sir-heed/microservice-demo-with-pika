from django.db.utils import IntegrityError
from .models import Product, ProductUser
from .producer import publish
from .serializers import ProductSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class LikeView(APIView):
    def get(self, _, pk):
        req = requests.get('http://127.0.0.1:8000/api/user')
        response = req.json()
        try:
            product = Product.objects.get(pk=pk)
            product_user = ProductUser.objects.create(user_id=response['id'], product_id=pk)
            publish('product_liked', product.product_id)
            return Response({
                'messsage': 'Success'
            })
        except IntegrityError:
            return Response({
                'message': 'You already liked this product'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(req.json())