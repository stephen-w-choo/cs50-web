# Generated by Django 4.0.4 on 2022-05-23 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionitem',
            name='description',
            field=models.TextField(default='No description provided'),
            preserve_default=False,
        ),
    ]
