from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Tax(models.Model):
    """Модель налогов."""

    display_name = models.CharField(
        verbose_name='Название',
        max_length=100,
        unique=True
    )
    inclusive = models.BooleanField(
        verbose_name='Включено в цену?',
        default=True
    )
    percentage = models.PositiveSmallIntegerField(
        verbose_name='Величина налога (%)',
        validators=(
            MaxValueValidator(100, message='Максимальная скидка - 100%'),
            MinValueValidator(1, message='Минимальная скидка - 100%')
        )
    )

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return f'{self.display_name} ({self.percentage}%)'


class Item(models.Model):
    """Модель товаров."""

    class CurrencyType(models.TextChoices):
        """Валюты."""
        RUB = 'RUB', 'Российский рубль  '
        USD = 'USD', 'Американский доллар'

    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.CharField(verbose_name='Описание', max_length=255)
    price = models.IntegerField(verbose_name='Цена (коп)', default=0)
    tax = models.ForeignKey(
        Tax,
        verbose_name='Налог',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='item'
    )
    currency = models.CharField(
        verbose_name='Валюта',
        max_length=3,
        choices=CurrencyType.choices,
        default=CurrencyType.RUB
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_display_price(self):
        price = self.price / 100
        return f'{self.currency} {price:.2f}'


class Order(models.Model):
    """Модель заказов."""

    item = models.OneToOneField(
        Item,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='order',
        primary_key=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Discount(models.Model):
    """Модель скидок."""

    id = models.CharField(
        verbose_name='Код купона',
        max_length=100,
        primary_key=True
    )
    percent_off = models.PositiveSmallIntegerField(
        verbose_name='Величина скидки (%)',
        validators=(
            MaxValueValidator(100, message='Максимальная скидка - 100%'),
            MinValueValidator(1, message='Минимальная скидка - 1%')
        )
    )

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return f'{self.id} (-{self.percent_off}%)'
