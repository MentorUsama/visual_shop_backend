from customer.models.Province import Province
from django.db.models.fields.related import ForeignKey
from django.db import models
class City(models.Model):
    name = models.CharField(max_length=20)
    provinceId = ForeignKey(Province, on_delete=models.CASCADE,related_name="cities",verbose_name='Province')
    def __str__(self):
        return self.name
        