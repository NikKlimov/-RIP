from django.contrib import admin
from .models import Applications, AuthUser, Services


# Register your models here.
@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'modified_date')

@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    pass
@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    pass