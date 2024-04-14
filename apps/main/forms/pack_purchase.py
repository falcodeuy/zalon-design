from django import forms
from django.utils.translation import gettext as _

from apps.main.models import PackSale, Customer


class PackPurchaseForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    business = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=100)

    class Meta:
        model = PackSale
        fields = ("pack",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("A customer with this email already exists.")
        return email

    def save(self, commit=True):
        pack = self.cleaned_data.get("pack")
        name = self.cleaned_data.get("name")
        business = self.cleaned_data.get("business")
        email = self.cleaned_data.get("email")
        phone = self.cleaned_data.get("phone")

        customer, created = Customer.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "business": business,
                "phone": phone,
            },
        )

        pack_sale = PackSale.objects.create(pack=pack, customer=customer)
        return pack_sale
