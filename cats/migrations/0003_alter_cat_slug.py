# Generated by Django 4.2.1 on 2024-04-07 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0002_alter_cat_options_cat_slug_alter_cat_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
