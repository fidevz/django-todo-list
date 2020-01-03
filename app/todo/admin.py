from django.contrib import admin
from . import models

class TaskAdmin(admin.ModelAdmin):
    list_display = ("title",  "created", "due_date")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Priority, PriorityAdmin)
