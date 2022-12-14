# Generated by Django 4.1.2 on 2022-11-12 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mart_name', models.CharField(blank=True, max_length=9, null=True)),
                ('name', models.CharField(blank=True, max_length=15, null=True)),
                ('product_id', models.CharField(blank=True, max_length=10, null=True)),
                ('expirydate', models.CharField(blank=True, db_column='Expirydate', max_length=11, null=True)),
                ('cp', models.CharField(blank=True, max_length=4, null=True)),
                ('sp', models.CharField(blank=True, max_length=5, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dataset',
            },
        ),
        migrations.CreateModel(
            name='extendedProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('location', models.CharField(max_length=20)),
                ('manager_name', models.CharField(max_length=30)),
            ],
        ),
    ]
