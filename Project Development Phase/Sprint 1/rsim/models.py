from django.db import models

# Create your models here.
class Dataset(models.Model):
    mart_name = models.CharField(max_length=9, blank=True, null=True)
    name = models.CharField(max_length=15, blank=True, null=True)
    product_id = models.CharField(max_length=10, blank=True, null=True)
    expirydate = models.CharField(db_column='Expirydate', max_length=11, blank=True, null=True)  # Field name made lowercase.
    cp = models.CharField(max_length=4, blank=True, null=True)
    sp = models.CharField(max_length=4, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'dataset'   
