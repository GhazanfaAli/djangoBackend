from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api.models import User

# Register your models here.


class UserModelAdmin(BaseUserAdmin):
    # The forms to add and change user instances
  

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name", "bio","is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","bio"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name","bio","password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)