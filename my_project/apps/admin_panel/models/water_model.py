from django.db import models

class Water(models.Model):
    source = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.source