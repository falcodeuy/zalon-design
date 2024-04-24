from django import forms
from django.utils.translation import gettext as _

from apps.main.models import CustomerReview, Customer


class CustomerReviewForm(forms.ModelForm):
    review = forms.CharField(
        label=_("Reseña"),
        widget=forms.Textarea(  # Use Textarea widget for multiline input
            attrs={
                "placeholder": "Escribe tu reseña",
                "required": True,
                "class": "input",
                "rows": 4,  # Set the number of visible rows for the textarea
            }
        ),
        required=True,
    )

    class Meta:
        model = CustomerReview
        fields = ("pack", "customer")

    def __init__(self, *args, **kwargs):
        pack_id = kwargs.pop("pack_id")
        customer_id = kwargs.pop("customer_id")
        super().__init__(*args, **kwargs)
        # We autoset packa and customer fields because we are passing them as arguments from the view
        self.fields["pack"].initial = pack_id
        self.fields["pack"].widget = forms.HiddenInput()
        self.fields["pack"].label = ""
        self.fields["customer"].initial = customer_id
        self.fields["customer"].widget = forms.HiddenInput()
        self.fields["customer"].label = ""
