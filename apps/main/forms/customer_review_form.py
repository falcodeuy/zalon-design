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

    score = forms.IntegerField(
        label=_("Puntuación"),
        widget=StarRatingWidget(),
        required=True,
    )

    class Meta:
        model = CustomerReview
        fields = ("pack", "customer")

    def __init__(self, *args, **kwargs):
        super(CustomerReviewForm, self).__init__(*args, **kwargs)
        self.fields["customer"].widget = forms.HiddenInput()
        self.fields["customer"].label = ""
        self.fields["pack"].widget = forms.HiddenInput()
        self.fields["pack"].label = ""

    def save(self, commit=True):
        email = self.cleaned_data.get("email")
        pack = self.cleaned_data.get("pack")

        try:
            customer = Customer.objects.get(email=email)
            pack = Pack.objects.get(id=pack.id)
        except Customer.DoesNotExist or Pack.DoesNotExist:
            return None

        review = super().save(commit=False)
        review.customer = customer
        review.pack = pack

        if commit:
            review.save()

        return review
