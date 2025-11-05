from django.db import models
from django.utils.text import slugify
from PIL import Image
import os

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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resim varsa otomatik olarak resize et
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)
            
            # Slider için ideal boyut: 1920x800
            target_width = 1920
            target_height = 800
            
            # Orijinal boyutları al
            original_width, original_height = img.size
            
            # Aspect ratio'yu koru ve crop et
            aspect_ratio = target_width / target_height
            original_aspect = original_width / original_height
            
            if original_aspect > aspect_ratio:
                # Resim daha geniş - yüksekliğe göre ölçekle, genişliği crop et
                new_height = target_height
                new_width = int(original_width * (target_height / original_height))
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Ortadan crop et
                left = (new_width - target_width) // 2
                img = img.crop((left, 0, left + target_width, target_height))
            else:
                # Resim daha dar - genişliğe göre ölçekle, yüksekliği crop et
                new_width = target_width
                new_height = int(original_height * (target_width / original_width))
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Ortadan crop et
                top = (new_height - target_height) // 2
                img = img.crop((0, top, target_width, top + target_height))
            
            # JPEG formatında kaydet
            img = img.convert('RGB')
            img.save(img_path, 'JPEG', quality=90, optimize=True)
    
    @property
    def image_dimensions(self):
        """Resim boyutlarını döndür"""
        if self.image:
            try:
                img = Image.open(self.image.path)
                return f"{img.size[0]}x{img.size[1]}"
            except:
                return "Bilinmiyor"
        return "Resim yok"
