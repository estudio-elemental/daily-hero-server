from django.contrib import admin
from .models import Hero


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'hp', 'max_hp', 'attack', 'defense', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Básicas', {
            'fields': ('level', 'exp')
        }),
        ('Atributos de Combate', {
            'fields': ('hp', 'max_hp', 'attack', 'defense')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def save_model(self, request, obj, form, change):
        # Garantir que HP não seja negativo
        if obj.hp < 0:
            obj.hp = 0
        super().save_model(request, obj, form, change)
