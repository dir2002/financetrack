from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskkAdmin(admin.ModelAdmin):
    list_display =  ('id', 'name', 'description', 'deadline', 'finscore', 'is_active', 'add_date')
    search_fields = ('name', 'description', 'deadline', 'finscore', 'is_active', 'add_date')
    list_filter = ('is_active', 'deadline', 'finscore')