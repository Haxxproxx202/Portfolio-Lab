from django.contrib import admin
from .models import Institution, Category

@admin.register(Institution, Category)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", )
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", )
