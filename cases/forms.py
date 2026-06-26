from django import forms
from .models import UnknownCase, Message


class UnknownCaseForm(forms.ModelForm):
    """
    Форма для добавления неизвестного корпуса.
    Содержит только поле для загрузки фото.
    """
    class Meta:
        model = UnknownCase
        fields = ['photo']


class MessageForm(forms.ModelForm):
    """
    Форма для отправки сообщения о неизвестном корпусе.
    Содержит поля: имя отправителя и текст сообщения.
    """
    class Meta:
        model = Message
        fields = ['name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }
