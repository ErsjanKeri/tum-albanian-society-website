from django.core.management.base import BaseCommand
from django.test import Client
import json
import re


class Command(BaseCommand):
    help = 'Validate structured data (Schema.org) on all pages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Specific URL to validate (default: validate all main pages)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed schema information',
        )

    def handle(self, *args, **options):
        client = Client()
        
        # URLs to test
        if options['url']:
            urls = [('Custom', options['url'])]
        else:
            urls = [
                ('Homepage EN', '/'),
                ('Homepage SQ', '/sq/'),
                ('Homepage DE', '/de/'),
                ('Contact EN', '/contact/'),
                ('Contact SQ', '/sq/contact/'),
                ('Contact DE', '/de/contact/'),
            ]
        
        self.stdout.write(self.style.SUCCESS('=== Schema.org Validation Report ===\n'))
        
        total_pages = 0
        total_schemas = 0
        valid_schemas = 0
        
        for page_name, url in urls:
            total_pages += 1
            self.stdout.write(f'Testing {page_name}: {url}')
            
            try:
                response = client.get(url)
                
                if response.status_code != 200:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Page not accessible (Status: {response.status_code})')
                    )
                    continue
                
                content = response.content.decode('utf-8')
                
                # Extract JSON-LD blocks
                json_ld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
                json_blocks = re.findall(json_ld_pattern, content, re.DOTALL)
                
                page_schemas = len(json_blocks)
                total_schemas += page_schemas
                page_valid = 0
                
                self.stdout.write(f'  Found {page_schemas} JSON-LD blocks')
                
                for i, block in enumerate(json_blocks, 1):
                    try:
                        clean_json = block.strip()
                        parsed = json.loads(clean_json)
                        schema_type = parsed.get('@type', 'Unknown')
                        
                        # Basic validation
                        required_fields = ['@context', '@type']
                        if all(field in parsed for field in required_fields):
                            self.stdout.write(f'    ✓ Block {i}: Valid {schema_type} schema')
                            page_valid += 1
                            valid_schemas += 1
                            
                            if options['verbose']:
                                # Show additional details for verbose mode
                                if schema_type == 'Organization':
                                    name = parsed.get('name', 'N/A')
                                    url_field = parsed.get('url', 'N/A')
                                    self.stdout.write(f'      - Name: {name}')
                                    self.stdout.write(f'      - URL: {url_field}')
                                elif schema_type == 'WebPage':
                                    name = parsed.get('name', 'N/A')
                                    lang = parsed.get('inLanguage', 'N/A')
                                    self.stdout.write(f'      - Name: {name}')
                                    self.stdout.write(f'      - Language: {lang}')
                                elif schema_type == 'Event' or schema_type == 'EventSeries':
                                    name = parsed.get('name', 'N/A')
                                    self.stdout.write(f'      - Name: {name}')
                        else:
                            self.stdout.write(
                                self.style.WARNING(f'    ⚠ Block {i}: Missing required fields')
                            )
                            
                    except json.JSONDecodeError as e:
                        self.stdout.write(
                            self.style.ERROR(f'    ✗ Block {i}: Invalid JSON - {str(e)[:50]}...')
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'    ✗ Block {i}: Error - {str(e)[:50]}...')
                        )
                
                if page_valid == page_schemas:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ All schemas valid on this page\n'))
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ {page_valid}/{page_schemas} schemas valid\n')
                    )
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error testing page: {e}\n'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('=== Validation Summary ==='))
        self.stdout.write(f'Pages tested: {total_pages}')
        self.stdout.write(f'Total schemas: {total_schemas}')
        self.stdout.write(f'Valid schemas: {valid_schemas}')
        
        if valid_schemas == total_schemas:
            self.stdout.write(self.style.SUCCESS('✓ All structured data is valid!'))
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠ {total_schemas - valid_schemas} schemas need attention')
            )
        
        # SEO recommendations
        self.stdout.write('\n=== SEO Recommendations ===')
        self.stdout.write('• Test your structured data with Google\'s Rich Results Test:')
        self.stdout.write('  https://search.google.com/test/rich-results')
        self.stdout.write('• Validate with Schema.org validator:')
        self.stdout.write('  https://validator.schema.org/')
        self.stdout.write('• Monitor in Google Search Console for rich snippets')