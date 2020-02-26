from django.db import models

# Create your models here.
class Cloth(models.Model):
    # id = models.IntegerField(primary_key=True)
    brand = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    clothImg = models.URLField()
    price = models.CharField(max_length=100)
    category = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        """A string representation of the model."""
        return [self.id, self.title, self.crdate]