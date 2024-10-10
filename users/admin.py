from django.contrib import admin
from .models import Participant, Reservation

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0  

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'cin', 'participant_category', 'created_at', 'update_at')
    search_fields = ['username', 'email', 'cin']
    ordering = ['username']
    inlines = [ReservationInline]  

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('conference', 'participant', 'confirmed', 'reservation_date')
    search_fields = ['conference__title', 'participant__username']
    list_filter = ['confirmed']  
