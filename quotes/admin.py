from django.contrib import admin
from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """Interface d'administration pour les citations."""
    
    list_display = ('author', 'text_preview', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author')
    date_hierarchy = 'created_at'
    
    def text_preview(self, obj):
        """Affiche un aperçu du texte."""
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    
    text_preview.short_description = 'Aperçu'
