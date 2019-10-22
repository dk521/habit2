from django.contrib import admin
from .models import *
class HabitsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Habits._meta.fields]

    class Meta:
        model = Habits


class FilesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Files._meta.fields]

    class Meta:
        model = Files


admin.site.register(Habits, HabitsAdmin)
admin.site.register(Files, FilesAdmin)

