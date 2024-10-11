from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Conference
from users.models import Reservation
from django.db.models import Count

class ParticipantFilter(admin.SimpleListFilter):
    title="Participant count"
    parameter_name="participants"
    def lookups(self, request, model_admin):
        return ( 
            ('0', ('No participants')),
            ('more', ('More participants')),
        )
    
    def queryset(self, request, queryset):
        if (self.value() =='0'):
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        elif (self.value() == 'more'):
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)
        else:
            return queryset     

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 1
    readonly_fields = ('reservation_date', )
    can_delete = False

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'category', 'capacity', 'price')
    search_fields = ['title']
    ordering = ['start_date']
    list_filter = ['category', 'start_date', ParticipantFilter]
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

    inlines = [ReservationInline]

