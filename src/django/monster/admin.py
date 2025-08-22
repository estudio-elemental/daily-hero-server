from django.contrib import admin
from django.utils.html import format_html
from .models import Monster


@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'level', 'hp', 'attack', 'defense', 'exp_earn', 'image_preview', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['name']
    list_editable = ['hp', 'attack', 'defense', 'exp_earn']
    readonly_fields = ['created_at', 'updated_at', 'image_preview_large']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'level')
        }),
        ('Imagem', {
            'fields': ('image', 'image_preview_large'),
            'description': 'Faça upload da imagem do monstro. Tamanho recomendado: 400x400 pixels.'
        }),
        ('Atributos de Combate', {
            'fields': ('hp', 'attack', 'defense', 'exp_earn')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
    
    def save_model(self, request, obj, form, change):
        # Garantir que HP não seja negativo
        if obj.hp < 0:
            obj.hp = 0
        super().save_model(request, obj, form, change)

    def image_preview(self, obj):
        """Small image preview for list view"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "Sem imagem"
    image_preview.short_description = 'Imagem'

    def image_preview_large(self, obj):
        """Large image preview for edit view"""
        if obj.image:
            return format_html('<img src="{}" width="200" height="200" style="object-fit: cover; border-radius: 10px;" />', obj.image.url)
        return "Sem imagem"
    image_preview_large.short_description = 'Visualização da Imagem'
