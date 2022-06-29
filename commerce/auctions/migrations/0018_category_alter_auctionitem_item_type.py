# Generated by Django 4.0.4 on 2022-06-29 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_alter_auctionitem_watching'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='auctionitem',
            name='item_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
        ),
    ]
