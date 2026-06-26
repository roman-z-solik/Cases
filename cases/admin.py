from django.contrib import admin
from .models import Manufacturer, Case, UnknownCase, Message


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """
    Админка для производителей.
    """
    list_display = ('name',)
    ordering = ('name',)  # ← сортировка по алфавиту


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """
    Админка для корпусов с поиском, фильтром и кликабельной моделью.
    """
    list_display = ('manufacturer', 'model_link')  # ← заменили model_name на model_link
    list_filter = ('manufacturer',)  # ← фильтр по производителю (должен работать)
    search_fields = ('model_name', 'manufacturer__name')  # ← поиск по модели и производителю
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

    def model_link(self, obj):
        """
        Возвращает ссылку на редактирование корпуса по его названию.
        """
        from django.utils.html import format_html
        from django.urls import reverse
        url = reverse('admin:cases_case_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.model_name)
    model_link.short_description = 'Модель'  # ← заголовок колонки
    model_link.allow_tags = True  # ← разрешаем HTML в колонке


@admin.register(UnknownCase)
class UnknownCaseAdmin(admin.ModelAdmin):
    """
    Админка для неизвестных корпусов.
    """
    list_display = ('id', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)  # ← сначала новые


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Админка для сообщений.
    """
    list_display = ('unknown_case', 'name', 'created_at')
    ordering = ('-created_at',)  # ← сначала новые
