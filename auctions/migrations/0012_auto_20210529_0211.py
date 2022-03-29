# Generated by Django 3.1.7 on 2021-05-29 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_watchlistitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='currentBid_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
