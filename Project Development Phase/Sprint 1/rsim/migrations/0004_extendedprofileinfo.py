# Generated by Django 4.1.2 on 2022-11-05 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsim', '0003_initial'),
    ]

    operations = [
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
