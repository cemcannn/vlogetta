from django.db import models
from django.utils.text import slugify

# Create your models here.

class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama")
    image = models.ImageField(upload_to='slider_images/', verbose_name="Slider Görseli")
    link = models.CharField(max_length=200, blank=True, null=True, verbose_name="Link")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Slider"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
