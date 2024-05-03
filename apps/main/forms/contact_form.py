from django import forms
from django.utils.translation import gettext as _

from apps.main.models import ContactMsg
from apps.main.utils import send_contact_notification_email


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_("Nombre"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "Tu nombre y apellido",
                "required": True,
                "class": "input",
            }
        ),
        required=True,
    )
    email = forms.EmailField(
        label=_("Email de contacto"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Tu email",
                "class": "input",
            }
        ),
        required=True,
    )
    message = forms.CharField(
        label=_("Mensaje"),
        widget=forms.Textarea(
            attrs={
                "placeholder": "¿En qué podemos ayudarte?",
                "class": "textarea",
            }
        ),
        required=True,
    )

    class Meta:
        model = ContactMsg
        fields = ("name", "email", "message")

    def save(self):
        contact_msg = ContactMsg.objects.create(
            name=self.cleaned_data["name"],
            email=self.cleaned_data["email"],
            message=self.cleaned_data["message"],
        )
        send_contact_notification_email(contact_msg)
        return contact_msg
