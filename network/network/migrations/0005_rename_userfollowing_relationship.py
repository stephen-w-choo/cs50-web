# Generated by Django 4.0.4 on 2022-10-12 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_userfollowing_userfollowing_unique_followers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserFollowing',
            new_name='Relationship',
        ),
    ]
