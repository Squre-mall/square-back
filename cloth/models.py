from django.db import models
from django.utils import timezone

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

# Create your models here.
class Cloth(models.Model):
    # id = models.IntegerField(primary_key=True)
    brand = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    clothImg = models.URLField()
    price = models.CharField(max_length=100)
    category = models.IntegerField()

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Cloth, self).save(*args, **kwargs)


    def __str__(self):
        """A string representation of the model."""
        return [self.id, self.title, self.crdate]