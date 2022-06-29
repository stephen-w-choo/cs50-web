# Generated by Django 4.0.4 on 2022-06-29 03:37

import auctions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_auctionitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitem',
            name='highest_bidder',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='highest_bidder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionitem',
            name='image',
            field=models.ImageField(upload_to=auctions.models.AuctionItem.user_directory_path),
        ),
    ]
