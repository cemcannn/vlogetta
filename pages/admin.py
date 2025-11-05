from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Slider

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order', '-created_at')
    list_editable = ('is_active', 'order')
    
    readonly_fields = ('image_preview_large', 'slider_preview', 'image_info')
    
    fields = (
        'title', 
        'description', 
        'image', 
        'image_info',
        'image_preview_large',
        'slider_preview',
        'link', 
        'is_active', 
        'order'
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "Resim yok"
    image_preview.short_description = "Önizleme"
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<h4>Yüklenen Resim:</h4>'
                '<img src="{}" style="max-width: 400px; max-height: 200px; object-fit: cover; border: 1px solid #ddd; border-radius: 4px;" />'
                '</div>',
                obj.image.url
            )
        return "Henüz resim yüklenmemiş"
    image_preview_large.short_description = "Resim Önizleme"
    
    def slider_preview(self, obj):
        if obj.image:
            try:
                from PIL import Image
                img = Image.open(obj.image.path)
                width, height = img.size
                
                return format_html(
                    '<div style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 4px;">'
                    '<h4>Slider\'da Nasıl Görünecek:</h4>'
                    '<div style="position: relative; width: 400px; height: 166px; background-image: url({}); '
                    'background-size: cover; background-position: center; border-radius: 4px; overflow: hidden;">'
                    '<div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); '
                    'color: white; padding: 15px;">'
                    '<h3 style="margin: 0; font-size: 16px;">{}</h3>'
                    '<p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.9;">{}</p>'
                    '</div>'
                    '</div>'
                    '<small style="color: #666;">Gerçek boyut: {}x{}px → Otomatik olarak 1920x800px\'e ayarlandı</small>'
                    '</div>',
                    obj.image.url,
                    obj.title,
                    obj.description[:100] + "..." if len(obj.description) > 100 else obj.description,
                    width, height
                )
            except:
                return format_html(
                    '<div style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 4px;">'
                    '<h4>Slider\'da Nasıl Görünecek:</h4>'
                    '<div style="position: relative; width: 400px; height: 166px; background-image: url({}); '
                    'background-size: cover; background-position: center; border-radius: 4px; overflow: hidden;">'
                    '<div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); '
                    'color: white; padding: 15px;">'
                    '<h3 style="margin: 0; font-size: 16px;">{}</h3>'
                    '<p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.9;">{}</p>'
                    '</div>'
                    '</div>'
                    '<small style="color: #666;">Otomatik olarak 1920x800px\'e ayarlanacak</small>'
                    '</div>',
                    obj.image.url,
                    obj.title,
                    obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
                )
        return "Slider önizlemesi için önce resim yükleyin"
    slider_preview.short_description = "Slider Önizleme"
    
    def image_info(self, obj):
        if obj.image:
            try:
                from PIL import Image
                img = Image.open(obj.image.path)
                width, height = img.size
                file_size = obj.image.size
                
                return format_html(
                    '<div style="background: #e9ecef; padding: 10px; border-radius: 4px; margin: 5px 0;">'
                    '<strong>📸 Resim Bilgileri:</strong><br>'
                    '• Boyut: {}x{} piksel<br>'
                    '• Dosya boyutu: {:.1f} KB<br>'
                    '• Format: {}<br>'
                    '<span style="color: #28a745;">✅ Otomatik olarak 1920x800 boyutuna ayarlanacak</span>'
                    '</div>',
                    width, height,
                    file_size / 1024,
                    img.format or 'Bilinmiyor'
                )
            except Exception as e:
                return format_html(
                    '<div style="background: #f8d7da; padding: 10px; border-radius: 4px; color: #721c24;">'
                    'Resim bilgileri alınamadı: {}'
                    '</div>',
                    str(e)
                )
        return "Henüz resim yüklenmemiş"
    image_info.short_description = "Resim Detayları"
