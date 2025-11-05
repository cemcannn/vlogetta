from django.contrib import admin
from .models import Slider

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order', '-created_at')
    list_editable = ('is_active', 'order')
