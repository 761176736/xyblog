# Generated by Django 2.2.3 on 2019-10-13 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='昵称'),
        ),
    ]
