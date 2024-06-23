import math

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from PIL import Image
from apps.main.utils import send_confirmation_email
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
        verbose_name_plural = _("Galería")

    def save(self, *args, **kwargs):
        super(Illustration, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        img.save(self.image.path, optimize=True)

    def __str__(self):
        return self.image.url


class Customer(models.Model):
    name = models.CharField("Nombre", max_length=100)
    business = models.CharField("Empresa", max_length=100, null=True, blank=True)
    email = models.EmailField("Email")
    phone = models.CharField("Teléfono", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")

    def __str__(self):
        return f"{self.name} - {self.email}"


class Pack(models.Model):
    name = models.CharField("Nombre", max_length=100)
    subtitle = models.CharField("Descripción corta", max_length=350, default="")
    description = CKEditor5Field("Descripción")
    price = models.DecimalField("Precio de oferta", max_digits=6, decimal_places=0)
    strikethrough_price = models.DecimalField(
        "Precio regular", max_digits=6, decimal_places=0, null=True, blank=True
    )
    is_active = models.BooleanField("Activo", default=False)
    cover = models.ImageField("Carátula", upload_to="covers")
    instructions_file = models.FileField(
        "PDF de Pack",
        upload_to="instructions",
    )
    custom_url = models.CharField(
        "URL personalizada",
        max_length=200,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[\w-]+$",
                message="URL personalizada debe contener solo letras, números, guiones y guiones bajos.",
                code="invalid_custom_url",
            ),
        ],
    )

    def __str__(self):
        return self.name

    @property
    def score(self):
        """
        The average score of the reviews of the pack
        """
        reviews = self.reviews.all()
        if reviews:
            total_count = reviews.count()
            total_score = sum([review.score for review in reviews])
            average = total_score / total_count
            rounded_average = math.ceil(average)
            return rounded_average
        return 5

    @property
    def filled_stars(self):
        """
        Easy way to get the filled stars to display in the templates
        """
        return range(self.score)

    @property
    def empty_stars(self):
        """
        Easy way to get the empty stars to display in the templates
        """
        return range(5 - self.score)


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
    )
    score = models.PositiveSmallIntegerField(
        "Puntuación",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
    )

    class Meta:
        verbose_name = _("Reseña")
        verbose_name_plural = _("Reseñas")

    def __str__(self):
        return f"{self.customer} - {self.pack}"

    @property
    def filled_stars(self):
        """
        Easy way to get the filled stars to display in the templates
        """
        return range(self.score)

    @property
    def empty_stars(self):
        """
        Easy way to get the empty stars to display in the templates
        """
        return range(5 - self.score)


class Order(models.Model):
    pack = models.ForeignKey("Pack", on_delete=models.CASCADE, verbose_name="Pack")
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        verbose_name="Cliente",
        related_name="orders",
    )
    created_at = models.DateTimeField("Fecha", auto_now_add=True)
    is_reviewed = models.BooleanField("Tiene reseña", default=False)
    review_request_sent = models.BooleanField(
        "Solicitud de reseña enviada", default=False
    )

    class Meta:
        verbose_name = _("Orden")
        verbose_name_plural = _("Órdenes")

    def __str__(self):
        return f"{self.customer} - {self.pack} - {self.created_at}"


class ContactMsg(models.Model):
    name = models.CharField("Nombre", max_length=100)
    email = models.EmailField("Email")
    message = models.TextField("Mensaje")
    created_at = models.DateTimeField("Fecha", auto_now_add=True)

    class Meta:
        verbose_name = _("Mensaje de contacto")
        verbose_name_plural = _("Mensajes de contacto")

    def __str__(self):
        return f"{self.name} - {self.email}"


class Payment(models.Model):
    order = models.OneToOneField(
        "Order", on_delete=models.CASCADE, verbose_name="Orden", related_name="payment"
    )
    created_at = models.DateTimeField("Fecha de creación")
    last_modified = models.DateTimeField("Última modificación")
    amount = models.DecimalField("Monto", max_digits=6, decimal_places=0)
    payment_method = models.CharField("Método de pago", max_length=100)
    payment_type = models.CharField("Tipo de pago", max_length=100)
    payment_status = models.CharField("Estado de pago", max_length=100)
    payment_id = models.CharField("ID de pago", max_length=100)
    payment_provider = models.CharField("Proveedor de pago", max_length=100)

    class Meta:
        verbose_name = _("Pago")
        verbose_name_plural = _("Pagos")

    def save(self, *args, **kwargs):
        new_payment_status = kwargs.get("payment_status", self.payment_status)

        if new_payment_status == "approved":
            send_confirmation_email(self.order)
        elif new_payment_status == "cancelled" or new_payment_status == "rejected":
            print("Bad payment")
        else:
            print("Pending")
        super().save(*args, **kwargs)
