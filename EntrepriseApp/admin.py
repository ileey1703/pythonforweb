from django.contrib import admin
from .models import Entreprise, Utilisateur
from django.contrib.auth.admin import UserAdmin
from VehiculeApp.models import Vehicule
from config.admin import admin_site
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
class Vehiculeline(admin.TabularInline):
    model = Vehicule
    fields = ('immatriculation', 'type_vehicule','capacite_kg','disponible')
    extra = 1
    show_change_link = True
class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [Vehiculeline]
    list_display = ('raison_social', 'adresse','created_at', 'updated_at')
    search_fields = ('raison_social', 'adresse')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('raison_social', 'adresse')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

admin_site.register(Entreprise, EntrepriseAdmin)
admin_site.register(Utilisateur,useradmin)
