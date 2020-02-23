from django.db import models

# Create your models here.
class Cloth(models.Model):
    id = models.IntegerField(primary_key=True)
    brand = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    clothsImg = models.ImageField()
    price = models.CharField(max_length=100)
    category = models.IntegerField()

    def __str__(self):
        """A string representation of the model."""
        return self.title