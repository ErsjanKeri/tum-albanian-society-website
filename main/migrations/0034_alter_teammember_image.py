# Generated manually on 2025-01-18 to change image field to profile_image_url

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_upcomingevents_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='image',
        ),
        migrations.AddField(
            model_name='teammember',
            name='profile_image_url',
            field=models.URLField(help_text='Vendosni linkun e fotos së profilit (p.sh. nga LinkedIn, GitHub, apo ndonjë burim tjetër)', verbose_name='Link i Fotos së Profilit', default='https://via.placeholder.com/150'),
        ),
    ] 