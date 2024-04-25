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


class Customer(models.Model):
    name = models.CharField("Nombre", max_length=100)
    business = models.CharField("Empresa", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Teléfono", max_length=100)
    photo = models.ImageField("Foto", upload_to="customers", null=True, blank=True)

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")

    def __str__(self):
        return f"{self.name} - {self.email}"


class Pack(models.Model):
    name = models.CharField("Nombre", max_length=100)
    subtitle = models.CharField("Subtítulo", max_length=100, null=True, blank=True)
    description = CKEditor5Field("Descripción")
    price = models.DecimalField("Precio", max_digits=6, decimal_places=0)
    strikethrough_price = models.DecimalField(
        "Precio tachado", max_digits=6, decimal_places=0, null=True, blank=True
    )
    is_active = models.BooleanField("Activo", default=True)
    show_in_landing = models.BooleanField("Mostrar en landing", default=False)
    cover = models.ImageField("Carátula", upload_to="covers")

    def __str__(self):
        return self.name


class CustomerReview(models.Model):
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        verbose_name="Cliente",
        related_name="reviews",
    )
    review = models.TextField("Reseña")
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
        return f"{self.customer} - {self.pack}"


class PackSale(models.Model):
    pack = models.ForeignKey("Pack", on_delete=models.CASCADE, verbose_name="Pack")
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        verbose_name="Cliente",
        related_name="sales",
    )
    created_at = models.DateTimeField("Fecha", auto_now_add=True)

    class Meta:
        verbose_name = _("Venta")
        verbose_name_plural = _("Ventas")

    def __str__(self):
        return f"{self.customer} - {self.pack} - {self.created_at}"
