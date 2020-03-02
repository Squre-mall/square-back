from django.db import models
from django.utils import timezone
from django_mysql import models as mysqlModel

# Create your models here.
class Cloth(models.Model, mysqlModel.Model):
    # id = models.IntegerField(primary_key=True)
    productNo = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    clothImgSuffix = models.CharField(max_length=300)
    # pageUrl = models.URLField() # productNo로 대체
    price = mysqlModel.JSONField()
    # price = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Cloth, self).save(*args, **kwargs)

    def __str__(self):
        """A string representation of the model."""
        return '{} / {} / {} / {}'\
            .format(self.id, self.productNo, self.title, self.category)

class Cloth_Detail_Musinsa(models.Model):
    pass