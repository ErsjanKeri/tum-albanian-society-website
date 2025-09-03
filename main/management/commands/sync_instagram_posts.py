from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Sync Instagram posts automatically (for cron jobs)'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Starting Instagram sync...')
        
        try:
            # Call the main curation command with auto-fetch
            call_command('curate_albanian_students_posts', '--auto-fetch', '--limit=12')
            self.stdout.write(self.style.SUCCESS('✅ Instagram sync completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Instagram sync failed: {str(e)}'))