from django.contrib import admin
from .models import Manufacturer, Case, UnknownCase, Message


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)  # ← сортировка по алфавиту


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model_name')
    list_filter = ('manufacturer',)  # ← фильтр по производителю
    ordering = ('manufacturer__name', 'model_name')  # ← сортировка по производителю, затем по модели

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
    ordering = ('-created_at',)  # ← сначала новые


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('unknown_case', 'name', 'created_at')
    ordering = ('-created_at',)  # ← сначала новые
