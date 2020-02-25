# Generated by Django 3.0.3 on 2020-02-25 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='news url', max_length=200)),
                ('url', models.CharField(help_text='news url', max_length=200)),
                ('image_url', models.CharField(help_text='news url', max_length=200)),
            ],
        ),
    ]
