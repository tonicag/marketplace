from django.contrib import admin
from django.urls import path, include
from .views import homepage_view, create_post, view_post, edit_post, order_post, view_orders

urlpatterns = [
    path('',homepage_view,name='home'),
    path('posts/add',create_post,name='create_post'),
    path('posts/<int:id>', view_post, name="view_post"),
    path('posts/<int:id>/edit', edit_post, name="edit_post"),
    path('posts/<int:id>/order', order_post, name="order_post"),
    path('orders/',view_orders,name="view_orders")
]
