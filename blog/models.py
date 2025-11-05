from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kategori Adı")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name="Kategori", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPostImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post Image'
        verbose_name_plural = 'Blog Post Images'

    def __str__(self):
        return f"{self.blog_post.name} - Image {self.id}"