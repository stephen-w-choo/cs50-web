# Generated by Django 4.0.4 on 2022-05-24 00:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auctioncomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctioncomment',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
