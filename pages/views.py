from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Slider
from blog.models import BlogPost

# def index(request):
#     return render(request, 'index.html')

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(is_active=True)
        context['posts'] = BlogPost.objects.filter(is_active=True)[:6]
        context['trending_posts'] = BlogPost.objects.filter(is_active=True, is_trending=True)[:5]
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'

