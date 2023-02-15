from core.models import Post
from core.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
import requests

# Create your views here.
class PostAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        # return Response(serializer.data)
        return Response([self.formatPost(p) for p in posts])

    def formatPost(self, post):
        comments = requests.get(f'http://localhost:8001/api/posts/{post.id}/comments').json()
        return {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'comments': comments
        }

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)