from django import forms

from .models import MessageContact


class MessageContactForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ("nom", "email", "message")
        widgets = {
            "nom": forms.TextInput(
                attrs={
                    "autocomplete": "name",
                    "placeholder": "Votre nom",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "autocomplete": "email",
                    "placeholder": "vous@exemple.com",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Racontez-nous ce que vous souhaitez partager...",
                }
            ),
        }
