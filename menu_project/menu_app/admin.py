from django.contrib import admin
from .models import Menu, MenuItem

# определение формы для пунктов меню
class MenuItemInline(admin.StackedInline):
    model = MenuItem
    extra = 1

# админская форма для меню с встроенными пунктами меню
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]

# регистрация модели
admin.site.register(Menu, MenuAdmin)
