from django.db import models
class Tags(models.Model):
    name=models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Tags, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Tags"
        