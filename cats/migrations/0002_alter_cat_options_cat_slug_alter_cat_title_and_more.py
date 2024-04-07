# Generated by Django 4.2.1 on 2024-04-07 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cat',
            options={'ordering': ['-time_create']},
        ),
        migrations.AddField(
            model_name='cat',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='cat',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
        migrations.AddIndex(
            model_name='cat',
            index=models.Index(fields=['-time_create'], name='cats_cat_time_cr_044b61_idx'),
        ),
    ]
