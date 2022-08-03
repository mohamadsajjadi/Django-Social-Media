from django.contrib import admin
from .models import Relation


# Register your models here.
@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user']
