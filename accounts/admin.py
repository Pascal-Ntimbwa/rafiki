from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html


class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "date_joined",
        "last_login",
        "is_active",
        "is_admin",
        "is_staff",
        "is_seller",
        "is_customer",
    )
    search_fields = (
        "email",
        "username",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
    )
    ordering = ("-date_joined",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)



class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50%;" />'.format(object.profile_picture.url))
    thumbnail.short_description = "Profile Picture"
    
    
    list_display = (
        "thumbnail",
        "user",
        "city",
        "state",
        "country",
        "profile_picture",
    )
    search_fields = ("user",)
    readonly_fields = ()
    ordering = ("user",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(UserProfile, UserProfileAdmin)
