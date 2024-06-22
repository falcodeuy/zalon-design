from typing import Any
from django import forms
from django.forms.widgets import NumberInput
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from apps.main.models import CustomerReview, Customer, Pack
from django.forms.renderers import BaseRenderer


class StarRatingWidget(NumberInput):
    template_name = "main/widgets/star_rating.html"


class CustomerReviewForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Escribe tu email",
                "required": True,
                "class": "input",
            }
        ),
        required=True,
    )

    score = forms.IntegerField(
        label="",
        widget=StarRatingWidget(),
        required=True,
    )

    review = forms.CharField(
        label=_("Reseña"),
        widget=forms.Textarea(
            attrs={
                "placeholder": "Escribe tu reseña",
                "required": True,
                "class": "textarea",
                "rows": 4,
            }
        ),
        required=True,
    )

    class Meta:
        model = CustomerReview
        fields = ("pack", "customer")

    def __init__(self, *args, **kwargs):
        super(CustomerReviewForm, self).__init__(*args, **kwargs)
        self.fields["customer"].widget = forms.HiddenInput()
        self.fields["customer"].label = ""
        self.fields["customer"].required = False
        self.fields["pack"].widget = forms.HiddenInput()
        self.fields["pack"].label = ""

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            raise forms.ValidationError(_("No se encontró un cliente con este email"))
        return email

    def save(self):
        customer_email = self.cleaned_data.get("email")
        customer = Customer.objects.get(email=customer_email)
        pack = self.cleaned_data.get("pack")
        score = self.cleaned_data.get("score")
        review = self.cleaned_data.get("review")
        customer_review = CustomerReview(
            pack=pack, customer=customer, score=score, review=review
        )
        customer_review.save()
        return customer_review
