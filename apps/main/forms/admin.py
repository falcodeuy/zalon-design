from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _


from apps.main.models import Pack, Illustration


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data and initial:
            return initial
        return data


class PackAdminForm(forms.ModelForm):
    class Meta:
        model = Pack
        fields = (
            "name",
            "price",
            "strikethrough_price",
            "subtitle",
            "description",
            "cover",
            "is_active",
            "instructions_file",
            "custom_url",
        )

    subtitle = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6}),
        label=_("Descripción corta"),
        required=False,
    )

    illustrations = MultipleFileField(
        widget=MultipleFileInput(),
        label=_("Agregar a galería"),
        required=True,
    )

    def clean_illustrations(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("illustrations"):
            validate_image_file_extension(upload)

    def save_illustrations(self, pack):
        """Process each uploaded image."""
        for upload in self.files.getlist("illustrations"):
            illustration = Illustration(pack=pack, image=upload)
            illustration.save()
