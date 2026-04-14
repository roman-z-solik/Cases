from django.contrib import admin
from .models import Manufacturer, Case, UnknownCase, Message

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model_name')
    fieldsets = (
        (None, {
            'fields': ('manufacturer', 'model_name')
        }),
        ('Фотографии', {
            'fields': ('photo', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6'),
            'description': 'Основное фото обязательно. Остальные - по желанию'
        }),
    )

@admin.register(UnknownCase)
class UnknownCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('unknown_case', 'name', 'created_at')
