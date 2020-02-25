# Generated by Django 3.0.3 on 2020-02-25 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20200224_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.CharField(default='Trend', help_text='image_url url', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='image_url',
            field=models.CharField(help_text='image_url url', max_length=200),
        ),
    ]
