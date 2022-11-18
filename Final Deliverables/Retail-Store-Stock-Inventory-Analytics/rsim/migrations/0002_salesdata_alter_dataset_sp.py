# Generated by Django 4.1.2 on 2022-11-14 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsim', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesData',
            fields=[
                ('slno', models.AutoField(db_column='SLNO', primary_key=True, serialize=False)),
                ('mart_name', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('product', models.CharField(max_length=30)),
                ('sales', models.CharField(max_length=6)),
                ('product_id', models.CharField(db_column='product ID', max_length=10)),
            ],
            options={
                'db_table': 'sales_data',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='dataset',
            name='sp',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]