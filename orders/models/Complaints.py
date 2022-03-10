from django.db import models
from orders.models.Order import Order

class Complaints(models.Model):
    orderId = models.OneToOneField(
        Order,verbose_name='Order', on_delete=models.CASCADE, related_name="complaints")
    complaintStatus = models.CharField(verbose_name='Complaint',max_length=50, choices=(
        ("pending", "PENDING"), ("solved", "SOLVED")), default="pending")  # should use regular expression
    class Meta:
        verbose_name_plural = "Complaints"
        