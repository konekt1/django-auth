from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "email", "first_name", "last_name", "role", "is_admin"]
    list_filter = ["is_admin", "is_verified"]
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "role"]}),
        ("Permissions", {"fields": ["is_admin", "is_verified"]}),
        ('OTP', {'fields': ('otp',)}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["first_name", "last_name", "email", "password1", "password2", "role", "otp", "is_verified"],
            },
        ),
        
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []



class RecruiterModelAdmin(admin.ModelAdmin):
    list_display = ('id','company_size', 'established_year', 'company_website', 'company_url')
    fields = ('company_size', 'established_year', 'company_website', 'company_url', 'company_mission', 'about_us')

    def id(self, obj):
        return obj.user.id

class InternModelAdmin(admin.ModelAdmin):
    list_display = ("user_id", "user_email", "get_first_name", "get_last_name", "phone_number", "current_location", "intern_category")
    fields = ("phone_number", "current_location", "intern_category")

    def user_id(self, obj):
        return obj.user.id

    def user_email(self, obj):
        return obj.user.email
    
    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    user_id.short_description = "User ID"
    user_email.short_description = "User Email"

    get_first_name.short_description = "First Name"
    get_last_name.short_description = "Last Name"

# Now register the new ModelAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(InternProfile, InternModelAdmin)
admin.site.register(RecruiterProfile, RecruiterModelAdmin)
