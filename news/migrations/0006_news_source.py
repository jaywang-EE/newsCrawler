# Generated by Django 3.0.3 on 2020-05-04 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20200328_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='source',
            field=models.CharField(help_text='source', max_length=40, null=True),
        ),
    ]
