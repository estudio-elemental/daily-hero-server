from django.contrib import admin
from .models import Fight

@admin.register(Fight)
class FightAdmin(admin.ModelAdmin):
    list_display = ('id', 'hero_id', 'monster_id', 'turn', 'winner')
    search_fields = ('hero_id', 'monster_id', 'winner')
    list_filter = ('turn', 'winner')
