from django import forms
from django.utils.translation import gettext as _
from apps.main.models import Order, Customer


class OrderForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        label=_("Nombre"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "Introduce tu nombre y apellido",
                "required": True,
                "class": "input",
            }
        ),
        required=True,
    )
    business = forms.CharField(
        max_length=100,
        label=_("Empresa"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "Introduce el nombre de tu negocio",
                "class": "input",
            }
        ),
        required=False,
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": "La dirección a la que enviaremos tu compra",
                "class": "input",
            }
        ),
        required=True,
    )
    phone = forms.CharField(
        max_length=100,
        label=_("Teléfono"),
        widget=forms.TextInput(attrs={"placeholder": "Opcional", "class": "input"}),
    )

    class Meta:
        model = Order
        fields = ("pack",)

    def __init__(self, *args, **kwargs):
        pack_id = kwargs.pop("pack_id")
        super().__init__(*args, **kwargs)
        # We set the initial value of the pack field to the pack_id passed as an argument from the view. And hide it
        self.fields["pack"].initial = pack_id
        self.fields["pack"].widget = forms.HiddenInput()
        self.fields["pack"].label = ""

    def save(self):
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

        # If data customer just put is new, we update the customer data. We identify the customer by email
        if not created:
            customer.name = name
            customer.business = business
            customer.phone = phone
            customer.save()

        order = Order.objects.create(pack=pack, customer=customer)
        return order
