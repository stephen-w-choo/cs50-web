# Generated by Django 4.0.4 on 2022-05-24 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auctionitem_highest_bidder_auctionitem_sold_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitem',
            name='highest_bidder',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='highest_bidder', to=settings.AUTH_USER_MODEL),
        ),
    ]
