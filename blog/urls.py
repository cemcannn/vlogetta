from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_post_list, name='list'),
    path('category/<slug:category_slug>/', views.category_posts, name='category'),
    path('<slug:slug>/', views.blog_post_detail, name='detail'),
]