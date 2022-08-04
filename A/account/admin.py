from django.contrib import admin
from .models import Relation, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user']


class UserProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False


class ExtendsUserAdmin(UserAdmin):
    inlines = (UserProfileInLine,)


admin.site.unregister(User)
admin.site.register(User, ExtendsUserAdmin)
