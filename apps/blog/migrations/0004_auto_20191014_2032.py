# Generated by Django 2.2.3 on 2019-10-14 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article_view_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='thumbnail',
            field=models.CharField(max_length=32, null=True, verbose_name='缩略图'),
        ),
    ]
