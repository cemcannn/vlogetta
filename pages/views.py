from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Slider
from blog.models import BlogPost, Category

# def index(request):
#     return render(request, 'index.html')

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(is_active=True)
        
        # Kategorilere göre son paylaşımları al
        categories = Category.objects.filter(is_active=True).order_by('order', 'name')
        
        # Her kategori için son 5 postu al
        category_posts = {}
        for category in categories:
            posts = BlogPost.objects.filter(
                category=category, 
                is_active=True
            ).order_by("order", "-created_at")[:10]
            if posts.exists():  # Sadece postu olan kategorileri ekle
                category_posts[category.slug] = {
                    'category': category,
                    'posts': posts,
                    'main_post': posts.first() if posts else None,
                    'side_posts': posts[1:] if len(posts) > 1 else []
                }
        
        context['category_posts'] = category_posts
        context['posts'] = BlogPost.objects.filter(is_active=True)[:6]
        context['trending_posts'] = BlogPost.objects.filter(is_active=True, is_trending=True)[:5]
        
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'

