from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from orders.models.OrderedProduct import OrderedProduct

class Feedback(models.Model):
    rating = models.PositiveIntegerField(verbose_name='Feedback',
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(max_length=500,verbose_name='Description')
    orderedProductId = models.OneToOneField(
        OrderedProduct, on_delete=models.CASCADE,related_name="feedbacks",verbose_name='Ordered Product')

    def __str__(self):
        return str(self.rating)

    class Meta:
        verbose_name_plural = "Feedbacks"
        