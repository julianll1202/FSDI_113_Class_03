from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView

urlpatterns = [
    path('list/', PostListView.as_view(), name='list'),
    path('details/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('new/', PostCreateView.as_view(), name='new'),
]