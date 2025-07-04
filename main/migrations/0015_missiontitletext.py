# Generated by Django 5.1.7 on 2025-03-09 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_delete_landingpagetext_delete_slides'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissionTitleText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_sq', models.CharField(max_length=255, verbose_name='Titulli Shqip')),
                ('title_en', models.CharField(max_length=255, verbose_name='Title English')),
                ('title_de', models.CharField(max_length=255, verbose_name='Titel Deutsch')),
                ('mission_subtitle_sq', models.TextField(verbose_name='Përshkrimi Shqip')),
                ('mission_subtitle_en', models.TextField(verbose_name='Description English')),
                ('mission_subtitle_de', models.TextField(verbose_name='Beschreibung Deutsch')),
            ],
            options={
                'verbose_name_plural': 'Mission Title Section Translations',
            },
        ),
    ]
