from django.db import models
from django.utils import timezone

from django_mysql.models import ListTextField, JSONField

# Create your models here.
class Cloth(models.Model):
    # id = models.IntegerField(primary_key=True)
    productNo = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    clothImgSuffix = models.CharField(max_length=300)
    price = JSONField(default=dict)
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
    cloth = models.OneToOneField(
        Cloth,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    description = models.TextField(blank=True, null=True)
    season = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    monthlyPopularity = models.CharField(max_length=100)
    # detailImageUrlList = ListTextField(
    #     base_field=models.CharField(max_length=200),
    #     size=50,
    # )
    color = models.CharField(max_length=100)
    importation = models.CharField(max_length=100)
    manufacturingYM = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    sizeNweight = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    manufactured = models.CharField(max_length=100)
    asdirector = models.CharField(max_length=100)
    precautions = models.CharField(max_length=500)
    warrantyBasis = models.CharField(max_length=100)

    def __str__(self):
        """A string representation of the model."""
        return '{} / {} 에 대한 상세 정보'\
            .format(self.cloth_id, self.cloth.title)