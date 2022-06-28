# Generated by Django 4.0.4 on 2022-05-24 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auctionitem_watching_alter_auctioncomment_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionBid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time', models.DateTimeField()),
                ('auction_item', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionitem')),
                ('bidder', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
