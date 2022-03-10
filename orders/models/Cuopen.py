from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator

class Cuopen(models.Model):
    minPurchase = models.DecimalField(
        decimal_places=3,verbose_name='Minimum Purcase', max_digits=8, validators=[MinValueValidator(0)])
    expiryDate = models.DateField(verbose_name='Expiry Date')
    totalQuantity = models.IntegerField(verbose_name='Total Quantity',validators=[MinValueValidator(0)])
    discountPercentage = models.IntegerField(
        default=0,verbose_name='Discount', validators=[MinValueValidator(0)])
    cuopenCode = models.IntegerField(unique=True,verbose_name='Cuopen')

    def __str__(self):
        return f'{self.cuopenCode}: for purchase > {self.minPurchase} till: {self.expiryDate}'
    class Meta:
        verbose_name_plural = "Cuopens"
        