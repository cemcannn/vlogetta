from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import BlogPost, Category

def blog_post_list(request):
    posts_list = BlogPost.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        posts_list = posts_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts_list, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Get recent posts for sidebar
    recent_posts = BlogPost.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    return render(request, 'blog.html', {
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'search_query': search_query
    })

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    posts_list = BlogPost.objects.filter(category=category, is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        posts_list = posts_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts_list, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Get recent posts for sidebar
    recent_posts = BlogPost.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    return render(request, 'blog.html', {
        'category': category,
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'search_query': search_query
    })

def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_active=True)
    categories = Category.objects.filter(is_active=True)
    recent_posts = BlogPost.objects.filter(is_active=True).exclude(id=post.id).order_by('-created_at')[:5]
    
    return render(request, 'blog/detail.html', {
        'post': post,
        'categories': categories,
        'recent_posts': recent_posts
    })