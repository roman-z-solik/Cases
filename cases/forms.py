from django import forms
from .models import UnknownCase, Message

class UnknownCaseForm(forms.ModelForm):
    class Meta:
        model = UnknownCase
        fields = ['photo']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }
