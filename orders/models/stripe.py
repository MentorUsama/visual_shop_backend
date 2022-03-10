from django.db import models

class Stripe(models.Model):
    strip_client_id = models.CharField(max_length=500,blank=True,null=True,verbose_name='Strip id')
    stripe_client_secret=models.CharField(max_length=500,blank=True,null=True,verbose_name='Strip secret')
