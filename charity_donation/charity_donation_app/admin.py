from django.contrib import admin
from accounts.models import CustomUser
from charity_donation_app.models import Institution, Category


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff']



@admin.register(Institution)
class InstitutionAdminm(admin.ModelAdmin):
    list_display = ['name', 'type','description']





