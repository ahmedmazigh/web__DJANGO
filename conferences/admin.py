from django.contrib import admin
from .models import Conference

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'category', 'capacity', 'price')
    search_fields = ['title']
    ordering = ['start_date']
    list_filter = ['category', 'start_date']
    readonly_fields = ('created_at', 'update_at')
    list_per_page=2

    autocomplete_fields = ['category'] # autocompletion 
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'description', 'category', 'location', 'capacity', 'price')
        }),
        ('Horaires', {
            'fields': ('start_date', 'end_date')
        }),
        ('Documents', {
            'fields': ('program',)
        }),
        ('Dates de suivi', {
            'fields': ('created_at', 'update_at'),
            'classes': ('collapse',) 
        }),
    )

