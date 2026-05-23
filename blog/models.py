from django.db import models
from django.utils.text import slugify
from PIL import Image, ImageFilter
import os

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
    order = models.IntegerField(default=0, verbose_name="Sıralama (kucuk=ust)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        # Resim varsa otomatik işleme uygula
        if self.image:
            self.process_cover_image()
            self.create_index_thumbnail()

    def create_index_thumbnail(self):
        """Index sayfası için 450x450 thumbnail oluştur"""
        if not self.image:
            return
            
        img_path = self.image.path
        img = Image.open(img_path)
        
        # Index thumbnail için boyutlar
        thumb_size = 450
        
        # Thumbnail dosya yolu oluştur
        base_name = os.path.splitext(img_path)[0]
        thumb_path = f"{base_name}_thumb.jpg"
        
        # Kare thumbnail oluştur
        thumb_img = self.create_square_thumbnail(img, thumb_size)
        
        # JPEG formatında kaydet
        thumb_img = thumb_img.convert('RGB')
        thumb_img.save(thumb_path, 'JPEG', quality=85, optimize=True)
    
    def create_square_thumbnail(self, img, size):
        """Kare thumbnail oluştur - ortadan crop"""
        original_width, original_height = img.size
        
        # Küçük boyutu bul
        min_dimension = min(original_width, original_height)
        
        # Ortadan kare crop et
        left = (original_width - min_dimension) // 2
        top = (original_height - min_dimension) // 2
        right = left + min_dimension
        bottom = top + min_dimension
        
        cropped = img.crop((left, top, right, bottom))
        
        # İstenen boyuta resize et
        return cropped.resize((size, size), Image.Resampling.LANCZOS)
    
    @property
    def index_thumbnail_url(self):
        """Index sayfası için thumbnail URL'i döndür"""
        if self.image:
            base_name = os.path.splitext(self.image.name)[0]
            thumb_name = f"{base_name}_thumb.jpg"
            
            # Thumbnail dosyasının varlığını kontrol et
            from django.conf import settings
            thumb_path = os.path.join(settings.MEDIA_ROOT, thumb_name)
            
            if os.path.exists(thumb_path):
                return f"{settings.MEDIA_URL}{thumb_name}"
            else:
                # Thumbnail yoksa orijinal resmi döndür
                return self.image.url
        return None

    def process_cover_image(self):
        """Blog kapak resmi için otomatik işleme"""
        if not self.image:
            return
            
        img_path = self.image.path
        img = Image.open(img_path)
        
        # Blog kapak resmi için ideal boyutlar
        target_width = 800  # Maksimum genişlik
        target_height = 600  # Maksimum yükseklik
        min_height = 400    # Minimum yükseklik
        
        # Orijinal boyutları al
        original_width, original_height = img.size
        
        # Eğer resim çok küçükse, arka plan bulanıklığı ile büyüt
        if original_height < min_height or original_width < target_width:
            img = self.create_padded_image(img, target_width, target_height)
        else:
            # Normal resize işlemi
            img = self.smart_resize(img, target_width, target_height)
        
        # JPEG formatında kaydet
        img = img.convert('RGB')
        img.save(img_path, 'JPEG', quality=85, optimize=True)
    
    def smart_resize(self, img, target_width, target_height):
        """Akıllı resize - aspect ratio koruyarak boyutlandır"""
        original_width, original_height = img.size
        
        # Hangi boyutun uygulanacağını hesapla
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height
        
        # Küçük oranı kullan (resim target boyutlarını aşmasın)
        ratio = min(width_ratio, height_ratio)
        
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def create_padded_image(self, img, target_width, target_height):
        """Küçük resimler için arka plan bulanıklığı ile padding ekle"""
        # Önce resmi mümkün olduğunca büyüt
        img_resized = self.smart_resize(img, target_width, target_height)
        
        # Arka plan için bulanık versiyon oluştur
        background = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        background = background.filter(ImageFilter.GaussianBlur(radius=15))
        
        # Hafif karartma ve renk tonu ekle
        background = background.point(lambda p: int(p * 0.3))  # %70 karart
        
        # Resize edilmiş resmi ortala
        new_img = Image.new('RGB', (target_width, target_height), (20, 20, 25))
        new_img.paste(background, (0, 0))
        
        # Orijinal resmi ortaya yerleştir
        x_offset = (target_width - img_resized.width) // 2
        y_offset = (target_height - img_resized.height) // 2
        
        new_img.paste(img_resized, (x_offset, y_offset))
        
        return new_img
    
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