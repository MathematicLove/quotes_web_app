from django.contrib import admin
from quotes.models import Source, Quote

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'image_url')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'source', 'weight', 'is_active', 'likes', 'dislikes', 'views', 'created_at')
    list_filter = ('is_active', 'source__kind')
    search_fields = ('text', 'source__title')
    autocomplete_fields = ('source',)

    def short_text(self, obj):
        return (obj.text[:70] + '…') if len(obj.text) > 70 else obj.text
