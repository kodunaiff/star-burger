from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Location(models.Model):
    address = models.CharField(
        verbose_name='адрес',
        max_length=200,
        unique=True,
    )
    latitude = models.FloatField(
        verbose_name="широта",
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ],
        null=True,
        blank=True,
    )
    longitude = models.FloatField(
        verbose_name="долгота",
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ],
        null=True,
        blank=True,
    )
    requested_at = models.DateTimeField(
        verbose_name="запрос координат осуществлен",
        default=timezone.now,
    )

    class Meta:
        verbose_name = "локация"
        verbose_name_plural = "локации"

    def __str__(self):
        return self.address
