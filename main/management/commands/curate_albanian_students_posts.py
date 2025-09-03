from django.core.management.base import BaseCommand
from main.models import InstagramPost
import requests
from datetime import datetime
import json
import re
from django.conf import settings


class Command(BaseCommand):
    help = 'Automatically fetch Instagram posts from Albanian Students TUM'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing posts')
        parser.add_argument('--auto-fetch', action='store_true', help='Auto-fetch from Instagram')
        parser.add_argument('--limit', type=int, default=12, help='Number of posts to fetch')
        parser.add_argument('--username', type=str, default='albanian_students_tum', help='Instagram username')

    def handle(self, *args, **options):
        if options['clear']:
            deleted_count = InstagramPost.objects.all().count()
            InstagramPost.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {deleted_count} existing posts'))

        if options['auto_fetch']:
            self.auto_fetch_posts(options['username'], options['limit'])
        else:
            self.create_sample_posts(options['limit'])

    def auto_fetch_posts(self, username, limit):
        """
        Auto-fetch Instagram posts using web scraping (no API required!)
        """
        self.stdout.write(f'🚀 Auto-fetching posts from @{username}...')
        
        try:
            # Method 1: Try Instagram Basic Display API if token exists
            access_token = getattr(settings, 'INSTAGRAM_ACCESS_TOKEN', None)
            if access_token:
                self.stdout.write('📡 Using Instagram API...')
                if self.fetch_with_api(access_token, limit):
                    return
            
            # Method 2: Web scraping fallback (no API required)
            self.stdout.write('🕷️ Using web scraping method...')
            self.fetch_with_scraping(username, limit)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Auto-fetch failed: {str(e)}'))
            self.stdout.write('📝 Creating sample posts instead...')
            self.create_sample_posts(limit)

    def fetch_with_api(self, access_token, limit):
        """Fetch using Instagram Basic Display API"""
        try:
            url = "https://graph.instagram.com/me/media"
            params = {
                'fields': 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp',
                'access_token': access_token,
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', [])
                
                created_count = 0
                for i, post_data in enumerate(posts):
                    if self.create_post_from_api_data(post_data, i + 1):
                        created_count += 1
                
                self.stdout.write(self.style.SUCCESS(f'✅ Created {created_count} posts from Instagram API'))
                return True
            else:
                self.stdout.write(self.style.WARNING(f'API returned {response.status_code}'))
                return False
                
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'API method failed: {str(e)}'))
            return False

    def fetch_with_scraping(self, username, limit):
        """
        Fetch using web scraping (Instagram's public endpoints)
        This doesn't require API tokens!
        """
        try:
            # Instagram's public JSON endpoint
            url = f"https://www.instagram.com/{username}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch Instagram page: {response.status_code}")
            
            # Extract JSON data from the page
            content = response.text
            json_match = re.search(r'window\._sharedData = ({.*?});', content)
            
            if not json_match:
                # Try alternative method
                json_match = re.search(r'"ProfilePage":\[{"graphql":{"user":({.*?})}}\]', content)
            
            if json_match:
                data = json.loads(json_match.group(1))
                posts = self.extract_posts_from_data(data, limit)
                
                created_count = 0
                for i, post_data in enumerate(posts):
                    if self.create_post_from_scraped_data(post_data, i + 1):
                        created_count += 1
                
                self.stdout.write(self.style.SUCCESS(f'✅ Created {created_count} posts from web scraping'))
            else:
                raise Exception("Could not extract post data from Instagram page")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Web scraping failed: {str(e)}'))
            self.stdout.write('📝 Creating sample posts instead...')
            self.create_sample_posts(limit)

    def extract_posts_from_data(self, data, limit):
        """Extract post data from Instagram's JSON response"""
        posts = []
        try:
            # Navigate through Instagram's data structure
            if 'entry_data' in data and 'ProfilePage' in data['entry_data']:
                user_data = data['entry_data']['ProfilePage'][0]['graphql']['user']
                media_data = user_data['edge_owner_to_timeline_media']['edges']
                
                for edge in media_data[:limit]:
                    node = edge['node']
                    posts.append({
                        'id': node.get('id'),
                        'shortcode': node.get('shortcode'),
                        'caption': node.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', ''),
                        'media_url': node.get('display_url'),
                        'thumbnail_url': node.get('thumbnail_src'),
                        'is_video': node.get('is_video', False),
                        'timestamp': node.get('taken_at_timestamp'),
                        'permalink': f"https://www.instagram.com/p/{node.get('shortcode')}/"
                    })
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Data extraction error: {str(e)}'))
        
        return posts

    def create_post_from_api_data(self, post_data, order):
        """Create InstagramPost from API data"""
        try:
            post_url = post_data.get('permalink')
            if not post_url or InstagramPost.objects.filter(post_url=post_url).exists():
                return False
            
            media_type = post_data.get('media_type', 'IMAGE')
            post_type = 'image'
            if media_type == 'VIDEO':
                post_type = 'video'
            elif media_type == 'CAROUSEL_ALBUM':
                post_type = 'carousel'
            
            InstagramPost.objects.create(
                post_url=post_url,
                caption=post_data.get('caption', '')[:1000],  # Limit caption length
                post_type=post_type,
                primary_media_url=post_data.get('thumbnail_url') or post_data.get('media_url'),
                media_urls=[post_data.get('media_url')] if post_data.get('media_url') else [],
                display_order=order,
                is_active=True
            )
            
            self.stdout.write(f'✅ Created post: {post_url}')
            return True
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to create post: {str(e)}'))
            return False

    def create_post_from_scraped_data(self, post_data, order):
        """Create InstagramPost from scraped data"""
        try:
            post_url = post_data.get('permalink')
            if not post_url or InstagramPost.objects.filter(post_url=post_url).exists():
                return False
            
            post_type = 'video' if post_data.get('is_video') else 'image'
            
            InstagramPost.objects.create(
                post_url=post_url,
                caption=post_data.get('caption', '')[:1000],
                post_type=post_type,
                primary_media_url=post_data.get('thumbnail_url') or post_data.get('media_url'),
                media_urls=[post_data.get('media_url')] if post_data.get('media_url') else [],
                display_order=order,
                is_active=True
            )
            
            self.stdout.write(f'✅ Created post: {post_url}')
            return True
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to create post: {str(e)}'))
            return False

    def create_sample_posts(self, limit):
        """Create sample posts as fallback"""
        sample_posts = [
            {
                'post_url': 'https://www.instagram.com/p/C_sample1/',
                'caption': '🇦🇱 Welcome to Albanian Students TUM! Join our vibrant community of Albanian students at Technical University of Munich. Together we achieve more! 💪 #AlbanianStudents #TUM #Munich #Community #Albania #Kosovo #Education #Engineering',
                'post_type': 'image',
                'primary_media_url': 'https://via.placeholder.com/600x600/E50914/FFFFFF?text=Albanian+Students+TUM+Welcome',
                'display_order': 1,
                'is_active': True
            },
            {
                'post_url': 'https://www.instagram.com/p/C_sample2/',
                'caption': '📚 Study group session at TUM library! Our members supporting each other through challenging engineering courses. This is what community looks like! 🤝 #StudyTogether #TUMLibrary #AlbanianStudents #AcademicSupport #Engineering #TeamWork #Success',
                'post_type': 'carousel',
                'primary_media_url': 'https://via.placeholder.com/600x600/1E88E5/FFFFFF?text=Study+Session+Main',
                'media_urls': [
                    'https://via.placeholder.com/600x600/1E88E5/FFFFFF?text=Study+Session+1',
                    'https://via.placeholder.com/600x600/43A047/FFFFFF?text=Group+Work',
                    'https://via.placeholder.com/600x600/FB8C00/FFFFFF?text=Library+Study'
                ],
                'display_order': 2,
                'is_active': True
            },
            {
                'post_url': 'https://www.instagram.com/p/C_sample3/',
                'caption': '🎉 Amazing turnout at our cultural evening! Traditional Albanian music, delicious food, and great company. Thank you to everyone who joined us! 🇦🇱✨ #CulturalEvening #AlbanianCulture #TraditionMeetsModern #Community #Munich #AlbanianStudents',
                'post_type': 'video',
                'primary_media_url': 'https://via.placeholder.com/600x600/8E24AA/FFFFFF?text=Cultural+Evening',
                'display_order': 3,
                'is_active': True
            },
            {
                'post_url': 'https://www.instagram.com/p/C_sample4/',
                'caption': '💻 Hackathon success! Our team developed an innovative solution for sustainable transportation. Proud of our Albanian students representing at TUM! 🏆 #Hackathon #Innovation #Sustainability #TechForGood #AlbanianTalent #TUM',
                'post_type': 'carousel',
                'primary_media_url': 'https://via.placeholder.com/600x600/FF5722/FFFFFF?text=Hackathon+Team',
                'media_urls': [
                    'https://via.placeholder.com/600x600/FF5722/FFFFFF?text=Hackathon+Team',
                    'https://via.placeholder.com/600x600/795548/FFFFFF?text=Presentation',
                    'https://via.placeholder.com/600x600/607D8B/FFFFFF?text=Award+Ceremony'
                ],
                'display_order': 4,
                'is_active': True
            },
            {
                'post_url': 'https://www.instagram.com/p/C_sample5/',
                'caption': '🌟 New semester, new opportunities! Welcome to all new Albanian students joining TUM. Our mentorship program is here to help you succeed! 📖 #NewSemester #Mentorship #WelcomeNewStudents #AlbanianStudents #TUM #Support #GrowthMindset',
                'post_type': 'image',
                'primary_media_url': 'https://via.placeholder.com/600x600/4CAF50/FFFFFF?text=Welcome+New+Students',
                'display_order': 5,
                'is_active': True
            },
            {
                'post_url': 'https://www.instagram.com/p/C_sample6/',
                'caption': '🏔️ Weekend hiking trip to the Bavarian Alps! Nothing beats combining studies with exploring beautiful Germany. Who\'s joining us next time? 🥾 #WeekendAdventure #BavarianAlps #Hiking #WorkLifeBalance #AlbanianStudents #ExploreGermany #Nature',
                'post_type': 'carousel',
                'primary_media_url': 'https://via.placeholder.com/600x600/2196F3/FFFFFF?text=Alpine+Adventure+1',
                'media_urls': [
                    'https://via.placeholder.com/600x600/2196F3/FFFFFF?text=Alpine+Adventure+1',
                    'https://via.placeholder.com/600x600/009688/FFFFFF?text=Mountain+View',
                    'https://via.placeholder.com/600x600/FF9800/FFFFFF?text=Group+Photo',
                    'https://via.placeholder.com/600x600/9C27B0/FFFFFF?text=Summit+Success'
                ],
                'display_order': 6,
                'is_active': True
            }
        ]
        
        created_count = 0
        for post_data in sample_posts[:limit]:
            if not InstagramPost.objects.filter(post_url=post_data['post_url']).exists():
                InstagramPost.objects.create(**post_data)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created post: {post_data["post_url"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Post already exists: {post_data["post_url"]}'))
        
        self.stdout.write(self.style.SUCCESS(f'📝 Created {created_count} sample posts'))
        
        if created_count > 0:
            self.stdout.write('\n🎯 Usage Instructions:')
            self.stdout.write('Manual posts: python manage.py curate_albanian_students_posts')
            self.stdout.write('Auto-fetch: python manage.py curate_albanian_students_posts --auto-fetch')
            self.stdout.write('Clear & fetch: python manage.py curate_albanian_students_posts --clear --auto-fetch')
            self.stdout.write('\n🚀 Auto-fetch will try API first, then web scraping, then fallback to samples!')