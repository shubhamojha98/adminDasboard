from django.db import models

class Waste(models.Model):
    type = models.CharField(max_length=100)
    disposal_method = models.CharField(max_length=255)

    def __str__(self):
        return self.type