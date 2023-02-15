from django.urls import path

from core.views import PostAPIView

urlpatterns = [
    path('posts', PostAPIView.as_view()),
]