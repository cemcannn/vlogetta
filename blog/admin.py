from django.contrib import admin
from django.utils.html import format_html
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
    list_display = ('name', 'image_preview', 'category', 'order', 'location', 'is_active', 'is_trending', 'created_at')
    list_editable = ("order", "is_active", "is_trending")
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'description', 'location')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BlogPostImageInline]
    ordering = ('-created_at',)
    readonly_fields = ('image_preview_large', 'blog_preview', 'image_info')
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug', 'description', 'location', 'category', 'is_active', 'is_trending')
        }),
        ('Kapak Görseli', {
            'fields': ('image', 'image_info', 'image_preview_large', 'blog_preview'),
            'description': '💡 Kapak görseli otomatik olarak 800x600 maksimum boyutlarına ayarlanır. Küçük resimler için arka plan bulanıklığı eklenir.'
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "Resim yok"
    image_preview.short_description = "Kapak"
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<h4>Kapak Görseli:</h4>'
                '<img src="{}" style="max-width: 400px; max-height: 300px; object-fit: cover; border: 1px solid #ddd; border-radius: 8px;" />'
                '</div>',
                obj.image.url
            )
        return "Henüz kapak görseli yüklenmemiş"
    image_preview_large.short_description = "Kapak Önizleme"
    
    def blog_preview(self, obj):
        if obj.image:
            return format_html(
                '<div style="margin: 10px 0; padding: 15px; background: #f8f9fa; border-radius: 8px;">'
                '<h4>Blog Kartında Nasıl Görünecek:</h4>'
                '<div style="max-width: 350px; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">'
                '<img src="{}" style="width: 100%; height: 200px; object-fit: cover;" />'
                '<div style="padding: 15px;">'
                '<h5 style="margin: 0 0 8px 0; color: #333; font-size: 16px; font-weight: 600;">{}</h5>'
                '<p style="margin: 0 0 10px 0; color: #666; font-size: 13px; line-height: 1.4;">{}</p>'
                '<div style="display: flex; justify-content: space-between; align-items: center;">'
                '<span style="color: #007cba; font-size: 12px; font-weight: 500;">{}</span>'
                '<span style="color: #999; font-size: 11px;">{}</span>'
                '</div>'
                '</div>'
                '</div>'
                '</div>',
                obj.image.url,
                obj.name,
                obj.description[:80] + "..." if len(obj.description) > 80 else obj.description,
                obj.category.name if obj.category else "Kategori Yok",
                obj.location
            )
        return "Blog kartı önizlemesi için kapak görseli yükleyin"
    blog_preview.short_description = "Blog Kartı Önizleme"
    
    def image_info(self, obj):
        if obj.image:
            try:
                from PIL import Image
                img = Image.open(obj.image.path)
                width, height = img.size
                file_size = obj.image.size
                
                # Resim kalitesi analizi
                if width >= 800 and height >= 400:
                    quality_status = '<span style="color: #28a745;">✅ Yüksek kalite</span>'
                elif width >= 600 and height >= 300:
                    quality_status = '<span style="color: #ffc107;">⚠️ Orta kalite</span>'
                else:
                    quality_status = '<span style="color: #dc3545;">📸 Düşük kalite - Arka plan bulanıklığı eklenecek</span>'
                
                # Thumbnail durumu
                import os
                from django.conf import settings
                base_name = os.path.splitext(obj.image.name)[0]
                thumb_name = f"{base_name}_thumb.jpg"
                thumb_path = os.path.join(settings.MEDIA_ROOT, thumb_name)
                
                if os.path.exists(thumb_path):
                    thumb_status = '<span style="color: #28a745;">✅ Index thumbnail mevcut (450x450)</span>'
                else:
                    thumb_status = '<span style="color: #dc3545;">❌ Index thumbnail bulunamadı</span>'
                
                return format_html(
                    '<div style="background: #e9ecef; padding: 12px; border-radius: 6px; margin: 5px 0;">'
                    '<strong>📸 Kapak Görseli Bilgileri:</strong><br>'
                    '• Orijinal boyut: {}x{} piksel<br>'
                    '• Dosya boyutu: {} KB<br>'
                    '• Format: {}<br>'
                    '• Blog kalitesi: {}<br>'
                    '• Index durumu: {}<br>'
                    '<small style="color: #666;">💡 Blog sayfası: Orijinal boyut | Index sayfası: 450x450 kare thumbnail</small>'
                    '</div>',
                    width, height,
                    round(file_size / 1024, 1),
                    img.format or 'Bilinmiyor',
                    quality_status,
                    thumb_status
                )
            except Exception as e:
                return format_html(
                    '<div style="background: #f8d7da; padding: 10px; border-radius: 4px; color: #721c24;">'
                    'Resim bilgileri alınamadı: {}'
                    '</div>',
                    str(e)
                )
        return "Henüz kapak görseli yüklenmemiş"
    image_info.short_description = "Görsel Detayları"

@admin.register(BlogPostImage)
class BlogPostImageAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('blog_post__name',)
    ordering = ('-created_at',)
