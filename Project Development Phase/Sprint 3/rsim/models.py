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

class extendedProfileInfo(models.Model):
    email = models.EmailField(unique=True)
    location = models.CharField(max_length = 20)
    manager_name = models.CharField(max_length = 30)

class SalesData(models.Model):
    slno = models.AutoField(db_column='SLNO', primary_key=True)  # Field name made lowercase.
    mart_name = models.CharField(max_length=20)
    year = models.IntegerField()
    month = models.IntegerField()
    product = models.CharField(max_length=30)
    sales = models.CharField(max_length=6)
    product_id = models.CharField(db_column='product ID', max_length=10)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'sales_data'

class RegularSales(models.Model):
    mart_name = models.CharField(max_length=20)
    prod_name = models.CharField(max_length=40)
    sales = models.IntegerField()
    date = models.CharField(max_length = 10)