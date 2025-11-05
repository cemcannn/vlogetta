# Trip modelini admin panelinden kaldırıyoruz
# Bu dosyayı boş bırakıyoruz çünkü artık Trip modelini admin panelinde göstermeyeceğiz

from django.contrib import admin
from .models import BlogPost, BlogPostImage, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_editable = ('is_active', 'order')

class BlogPostImageInline(admin.TabularInline):
    model = BlogPostImage
    extra = 1

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'description', 'location')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BlogPostImageInline]
    ordering = ('-created_at',)

@admin.register(BlogPostImage)
class BlogPostImageAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('blog_post__name',)
    ordering = ('-created_at',)
