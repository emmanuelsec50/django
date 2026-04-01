from .models import Members, Messages
from django import forms

class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['first_name', 'last_name', 'email', 'bio']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['content']