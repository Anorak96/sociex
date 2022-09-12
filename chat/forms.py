from django import forms
from .models import Chat
    
class ChatForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':109, 'style': 'padding: 10px; resize: none;'}))
    
    class Meta:
        model = Chat
        fields = [
            'body',
        ]
