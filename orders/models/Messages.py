
from django.db import models
from orders.models.Complaints import Complaints

class Messages(models.Model):
    complainId = models.ForeignKey(
        Complaints,verbose_name='Complaint', on_delete=models.CASCADE, related_name="messages")
    message = models.TextField(max_length=1000,verbose_name='Message')
    isAdmin = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name='Date')

    class Meta:
        get_latest_by = ['date', 'id']
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.message
        