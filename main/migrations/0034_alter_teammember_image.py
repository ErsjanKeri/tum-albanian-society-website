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
            field=models.URLField(help_text='Enter the profile image URL (e.g. from LinkedIn, GitHub, or other source)', verbose_name='Profile Image URL', default=''),
        ),
    ] 