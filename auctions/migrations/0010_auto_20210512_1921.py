# Generated by Django 3.1.7 on 2021-05-12 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210511_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingcomment',
            name='date',
            field=models.DateTimeField(),
        ),
    ]