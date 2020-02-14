from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User


class SandstormUserAdmin(UserAdmin):
    def has_module_permission(self, request):
        return False


class SandstormGroupAdmin(GroupAdmin):
    def has_module_permission(self, request):
        return False


admin.site.unregister(Group)
admin.site.register(Group, SandstormGroupAdmin)
admin.site.unregister(User)
admin.site.register(User, SandstormUserAdmin)
