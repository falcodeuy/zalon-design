from django.db import models
from django.utils.translation import gettext_lazy as _

from PIL import Image
from django_ckeditor_5.fields import CKEditor5Field


class Illustration(models.Model):
    image = models.ImageField("Imagen", upload_to="illustrations")
    pack = models.ForeignKey(
        "Pack",
        on_delete=models.CASCADE,
        verbose_name="Pack",
        related_name="illustrations",
        null=True,
    )

    class Meta:
        verbose_name = _("Ilustración")
        verbose_name_plural = _("Ilustraciones")

    def save(self, *args, **kwargs):
        super(Illustration, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 480 or img.width > 480:
            img.thumbnail((480, 480))
        img.save(self.image.path, quality=70, optimize=True)

    def __str__(self):
        return self.image.url


class Pack(models.Model):
    name = models.CharField("Nombre", max_length=100)
    subtitle = models.CharField("Subtítulo", max_length=100, null=True, blank=True)
    description = CKEditor5Field("Descripción")
    price = models.DecimalField("Precio", max_digits=6, decimal_places=2)
    is_active = models.BooleanField("Activo", default=True)
    show_in_landing = models.BooleanField("Mostrar en landing", default=False)
    cover = models.ImageField("Carátula", upload_to="covers")

    def __str__(self):
        return self.name


class CustomerReview(models.Model):
    name = models.CharField("Nombre", max_length=100)
    business = models.CharField("Empresa", max_length=100)
    review = models.TextField("Reseña")
    image = models.ImageField("Imagen", upload_to="reviews", null=True)
    pack = models.ForeignKey(
        "Pack",
        on_delete=models.CASCADE,
        verbose_name="Pack",
        related_name="reviews",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Reseña")
        verbose_name_plural = _("Reseñas")

    def __str__(self):
        return self.name
