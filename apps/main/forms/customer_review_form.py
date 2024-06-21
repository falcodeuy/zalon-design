from django import forms
from django.utils.translation import gettext as _
from apps.main.models import CustomerReview, Customer, Pack


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

    class Meta:
        model = CustomerReview
        fields = ("pack", "customer")

    def save(self, commit=True):
        # Get the email from the cleaned data
        email = self.cleaned_data.get("email")
        pack = self.cleaned_data.get("pack")

        try:
            customer = Customer.objects.get(email=email)
            pack = Pack.objects.get(id=pack.id)
        except Customer.DoesNotExist or Pack.DoesNotExist:
            return None

        # Create the CustomerReview instance but don't save it to the database yet
        review = super().save(commit=False)

        # Assign the customer and pack to the review
        review.customer = customer
        review.pack = pack

        # Save the review instance if commit is True
        if commit:
            review.save()

        return review
