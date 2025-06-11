from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Poll, PollOption

class PollOptionInline(admin.TabularInline):  # or StackedInline if you want a block layout
    model = PollOption
    extra = 2  # Number of extra blank options shown

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'id', 'created_by', 'end_date', 'created_at', 'is_active']
    list_filter = ['created_by', 'end_date', 'created_at']
    search_fields = ['question', 'created_by__email']
    inlines = [PollOptionInline]

    readonly_fields = ['id', 'created_by', 'created_at', 'is_active']
    fields = ['id', 'question', 'end_date', 'created_by', 'created_at', 'is_active']
@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ['poll', 'option_text']