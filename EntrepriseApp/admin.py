from django.contrib import admin
from .models import Entreprise, Utilisateur
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class useradmin(UserAdmin):
    list_display = ('user_id','username', 'email', 'is_active','is_superuser')
    list_editable = ('username','is_active','is_superuser')
    search_fields = ('user_id','username', 'email')
    list_filter = ('is_active','is_superuser','role')
    list_per_page = 2
    fieldsets = (
        ('Identification', {
            'fields': ('user_id','username', 'email', 'is_active','is_superuser')
        }),
        ('Permissions', {
            'fields': ('role','groups','user_permissions')
        }),
    )
    add_fildsets = (
        (
        None, {
            'classes': ('wide',),
            "fields":(
                'username','role','password1', 'password2','usable_password','email','telephone'
            )
        },
        ),
    ),
    
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_social', 'adresse', 'telephone', 'email', 'created_at', 'updated_at')
    search_fields = ('raison_social', 'adresse', 'telephone', 'email')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('raison_social', 'adresse', 'telephone', 'email')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Entreprise)
admin.site.register(Utilisateur,useradmin)
