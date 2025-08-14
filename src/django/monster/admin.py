from django.contrib import admin
from .models import Monster


@admin.register(Monster)
class MonsterAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'hp', 'attack', 'defense', 'exp_earn', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['name']
    list_editable = ['hp', 'attack', 'defense', 'exp_earn']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'level')
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
