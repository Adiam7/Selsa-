from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category

#@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'slug', 'parent', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)
