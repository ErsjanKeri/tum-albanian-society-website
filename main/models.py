from django.db import models
from django.utils import timezone 

from django.db import models


MONTH_CHOICES = [
    (0, 'January'), (1, 'February'), (2, 'March'), (3, 'April'),
    (4, 'May'), (5, 'June'), (6, 'July'), (7, 'August'), 
    (8, 'September'), (9, 'October'), (10, 'November'), (11, 'December')
]

# Translation dictionaries
MONTHS_SQ = {0: 'Janar', 1: 'Shkurt', 2: 'Mars', 3: 'Prill', 4: 'Maj', 5: 'Qershor', 6: 'Korrik', 7: 'Gusht', 8: 'Shtator', 9: 'Tetor', 10: 'Nëntor', 11: 'Dhjetor'}
MONTHS_EN = {0: 'January', 1: 'February', 2: 'March', 3: 'April', 4: 'May', 5: 'June', 6: 'July', 7: 'August', 8: 'September', 9: 'October', 10: 'November', 11: 'December'}
MONTHS_DE = {0: 'Januar', 1: 'Februar', 2: 'März', 3: 'April', 4: 'Mai', 5: 'Juni', 6: 'Juli', 7: 'August', 8: 'September', 9: 'Oktober', 10: 'November', 11: 'Dezember'}



class HeroSectionText(models.Model):
    name_sq = models.CharField(max_length=255, default="", verbose_name="Name of Association Shqip")
    name_en = models.CharField(max_length=255, default="", verbose_name="Name of Association English")
    name_de = models.CharField(max_length=255, default="", verbose_name="Name of Association Deutsch")

    st_org_sq = models.CharField(max_length=255, verbose_name="Teksti siper titullit Shqip")
    st_org_en = models.CharField(max_length=255, verbose_name="Teksti siper titullit English")
    st_org_de = models.CharField(max_length=255, verbose_name="Teksti siper titullit Deutsch")

    title_sq = models.CharField(max_length=255, verbose_name="Titulli Shqip")
    title_en = models.CharField(max_length=255, verbose_name="Title English")
    title_de = models.CharField(max_length=255, verbose_name="Titel Deutsch")

    subtitle_sq = models.TextField(verbose_name="Nën Titulli Shqip")
    subtitle_en = models.TextField(verbose_name="Subtitle English")
    subtitle_de = models.TextField(verbose_name="Untertitel Deutsch")
    
    start_sq = models.CharField(max_length=255, default="", verbose_name="Qe nga")
    start_en = models.CharField(max_length=255, default="", verbose_name="Since")
    start_de = models.CharField(max_length=255, default="", verbose_name="Ab")

    description_sq = models.TextField(verbose_name="Përshkrimi Shqip")
    description_en = models.TextField(verbose_name="Description English")
    description_de = models.TextField(verbose_name="Beschreibung Deutsch")

    join_us_btn_sq = models.CharField(max_length=255, verbose_name="Butoni Bashkohu Shqip", default="Bashkohu me ne")
    join_us_btn_en = models.CharField(max_length=255, verbose_name="Join Us Button English", default="Join Us")
    join_us_btn_de = models.CharField(max_length=255, verbose_name="Mitmachen Knopf Deutsch", default="Mitmachen")

    learn_more_btn_sq = models.CharField(max_length=255, verbose_name="Butoni Mëso më Shumë Shqip", default="Mëso më shumë")
    learn_more_btn_en = models.CharField(max_length=255, verbose_name="Learn More Button English", default="Learn More")
    learn_more_btn_de = models.CharField(max_length=255, verbose_name="Mehr Erfahren Knopf Deutsch", default="Mehr Erfahren")

    class Meta:
        verbose_name_plural = "Hero Section Translations"

    def __str__(self):
        return self.title_en

class AboutSection(models.Model):
    title_sq = models.CharField(max_length=255, verbose_name="Titulli Shqip")
    title_en = models.CharField(max_length=255, verbose_name="Title English")
    title_de = models.CharField(max_length=255, verbose_name="Titel Deutsch")

    category_sq = models.CharField(max_length=255, verbose_name="Kategoria Shqip")
    category_en = models.CharField(max_length=255, verbose_name="Category English")
    category_de = models.CharField(max_length=255, verbose_name="Kategorie Deutsch")

    description_sq = models.TextField(verbose_name="Përshkrimi Shqip")
    description_en = models.TextField(verbose_name="Description English")
    description_de = models.TextField(verbose_name="Beschreibung Deutsch")

    offer_title_sq = models.CharField(max_length=255, verbose_name="Çfarë Ofrojmë Shqip")
    offer_title_en = models.CharField(max_length=255, verbose_name="What We Offer English")
    offer_title_de = models.CharField(max_length=255, verbose_name="Was Wir Bieten Deutsch")

    offer_point1_sq = models.CharField(max_length=255, verbose_name="Pika 1 Shqip")
    offer_point1_en = models.CharField(max_length=255, verbose_name="Point 1 English")
    offer_point1_de = models.CharField(max_length=255, verbose_name="Punkt 1 Deutsch")

    offer_point2_sq = models.CharField(max_length=255, verbose_name="Pika 2 Shqip")
    offer_point2_en = models.CharField(max_length=255, verbose_name="Point 2 English")
    offer_point2_de = models.CharField(max_length=255, verbose_name="Punkt 2 Deutsch")

    offer_point3_sq = models.CharField(max_length=255, verbose_name="Pika 3 Shqip")
    offer_point3_en = models.CharField(max_length=255, verbose_name="Point 3 English")
    offer_point3_de = models.CharField(max_length=255, verbose_name="Punkt 3 Deutsch")

    offer_point4_sq = models.CharField(max_length=255, verbose_name="Pika 4 Shqip")
    offer_point4_en = models.CharField(max_length=255, verbose_name="Point 4 English")
    offer_point4_de = models.CharField(max_length=255, verbose_name="Punkt 4 Deutsch")

    button_text_sq = models.CharField(max_length=255, verbose_name="Teksti Butonit Shqip")
    button_text_en = models.CharField(max_length=255, verbose_name="Button Text English")
    button_text_de = models.CharField(max_length=255, verbose_name="Schaltflächen Text Deutsch")

    class Meta:
        verbose_name_plural = "About Section Translations"

    def __str__(self):
        return self.title_en



class MissionTitleText(models.Model):
    title_sq = models.CharField(max_length=255, verbose_name="Titulli Shqip")
    title_en = models.CharField(max_length=255, verbose_name="Title English")
    title_de = models.CharField(max_length=255, verbose_name="Titel Deutsch")

    mission_subtitle_sq = models.TextField(verbose_name="Përshkrimi Shqip")
    mission_subtitle_en = models.TextField(verbose_name="Description English")
    mission_subtitle_de = models.TextField(verbose_name="Beschreibung Deutsch")

    class Meta:
        verbose_name_plural = "Mission Title Section Translations"

    def __str__(self):
        return self.title_en


class MissionText(models.Model):
    index = models.IntegerField(default = 0, verbose_name = 'Renditja')
    title_sq = models.TextField(max_length = 512, verbose_name = 'Titulli Shqip')
    title_en = models.TextField(max_length = 512, verbose_name = 'Titulli Anglisht')
    title_de = models.TextField(max_length = 512, verbose_name = 'Titulli Gjermanisht')
    
    content_sq = models.TextField(verbose_name = 'Permbajtja Shqip')
    content_en = models.TextField(verbose_name = 'Permbajtja Anglisht')
    content_de = models.TextField(verbose_name = 'Permbajtja Gjermanisht')
    typeLogo = models.TextField(default = "", max_length = 40, verbose_name = 'Logo Class')

    class Meta: verbose_name_plural = 'Mision te Index Page'
    
    def __str__(self):
        return str(self.index) + ". " + self.title_en
    


class TeamMember(models.Model):
    index = models.IntegerField(default=0, verbose_name="Renditja")

    name = models.CharField(max_length=255, verbose_name="Emri")
    field_sq = models.CharField(max_length=255, verbose_name="Fusha Shqip")
    field_en = models.CharField(max_length=255, verbose_name="Field English")
    field_de = models.CharField(max_length=255, verbose_name="Feld Deutsch")

    description_sq = models.TextField(verbose_name="Përshkrimi Shqip")
    description_en = models.TextField(verbose_name="Description English")
    description_de = models.TextField(verbose_name="Beschreibung Deutsch")

    profile_image_url = models.URLField(verbose_name="Link i Fotos së Profilit", help_text="Vendosni linkun e fotos së profilit (p.sh. nga LinkedIn, GitHub, apo ndonjë burim tjetër)")
    
    class Meta:
        verbose_name_plural = "Team Members"

    def __str__(self):
        return self.name
    
class TeamMemberTitleText(models.Model):
    title_sq = models.CharField(max_length=255, verbose_name="Titulli Shqip")
    title_en = models.CharField(max_length=255, verbose_name="Title English")
    title_de = models.CharField(max_length=255, verbose_name="Titel Deutsch")

    description_sq = models.TextField(verbose_name="Përshkrimi Shqip")
    description_en = models.TextField(verbose_name="Description English")
    description_de = models.TextField(verbose_name="Beschreibung Deutsch")

    class Meta:
        verbose_name_plural = "Teksti për Anëtarët Themelues"

    def __str__(self):
        return self.title_en



class EventTitleText(models.Model):
    title_sq = models.CharField(max_length=200, verbose_name='Titulli Shqip')
    title_en = models.CharField(max_length=200, verbose_name='Titulli Anglisht')
    title_de = models.CharField(max_length=200, verbose_name='Titulli Gjermanisht')

    subtitle_sq = models.CharField(max_length=200, verbose_name='Nen Titulli Shqip')
    subtitle_en = models.CharField(max_length=200, verbose_name='Nen Titulli Anglisht')
    subtitle_de = models.CharField(max_length=200, verbose_name='Nen Titulli Gjermanisht')

    subsubtitle_sq = models.CharField(max_length=200, verbose_name='Nen nen Titulli Shqip')
    subsubtitle_en = models.CharField(max_length=200, verbose_name='Nen nen Titulli Anglisht')
    subsubtitle_de = models.CharField(max_length=200, verbose_name='Nen nen Titulli Gjermanisht')

    class Meta: 
        verbose_name_plural = 'Event Title Text te Index Page'

    def __str__(self):
        return f"{self.title_en}"



class UpcomingEvents(models.Model):
    # Date fields
    year = models.IntegerField(verbose_name="Year")
    month = models.IntegerField(choices=MONTH_CHOICES, verbose_name="Month")
    day = models.IntegerField(choices=[(i, i) for i in range(1, 32)], verbose_name="Day")
    
    # Content fields (keeping same structure)
    title_sq = models.CharField(max_length=200, verbose_name='Titulli Shqip')
    title_en = models.CharField(max_length=200, verbose_name='Titulli Anglisht')
    title_de = models.CharField(max_length=200, verbose_name='Titulli Gjermanisht')
    
    content_sq = models.TextField(verbose_name='Permbajtja Shqip')
    content_en = models.TextField(verbose_name='Permbajtja Anglisht')
    content_de = models.TextField(verbose_name='Permbajtja Gjermanisht')
    
    active = models.BooleanField(default=True, verbose_name='Aktiv') # if should be shown on the website


    # Helper methods
    def get_month_name(self, language='en'):
        # Return translated month name
        if language == 'sq':
            return MONTHS_SQ[self.month]
        elif language == 'en':
            return MONTHS_EN[self.month]
        elif language == 'de':
            return MONTHS_DE[self.month]
        return MONTHS_EN[self.month]

    # Properties for template access
    @property
    def month_name_sq(self):
        return MONTHS_SQ[self.month]
    
    @property
    def month_name_en(self):
        return MONTHS_EN[self.month]
    
    @property
    def month_name_de(self):
        return MONTHS_DE[self.month]

    def get_date(self):
        return f"{self.year}-{self.month}-{self.day}"
    
    class Meta:
        ordering = ['year', 'month', 'day']
    
    def __str__(self):
        return f"{self.get_month_name()} {self.day}, {self.year} - {self.title_en}"


class TechTitleText(models.Model):
    title_sq = models.CharField(max_length=200, verbose_name='Titulli Shqip')
    title_en = models.CharField(max_length=200, verbose_name='Titulli Anglisht')
    title_de = models.CharField(max_length=200, verbose_name='Titulli Gjermanisht')

    subtitle_sq = models.CharField(max_length=200, verbose_name='Nen Titulli Shqip')
    subtitle_en = models.CharField(max_length=200, verbose_name='Nen Titulli Anglisht')
    subtitle_de = models.CharField(max_length=200, verbose_name='Nen Titulli Gjermanisht')
    
    def __str__(self):
        return f"{self.title_en}"

class TechMissionText(models.Model):
    index = models.IntegerField(default=0, verbose_name='Renditja')
    
    typeLogo = models.CharField(default = "", max_length = 40, verbose_name = 'Logo Class')
    
    title_sq = models.CharField(max_length=512, verbose_name='Titulli Shqip')
    title_en = models.CharField(max_length=512, verbose_name='Titulli Anglisht')
    title_de = models.CharField(max_length=512, verbose_name='Titulli Gjermanisht')

    goal1_sq = models.CharField(max_length=512, verbose_name='Missioni 1 Shqip')
    goal1_en = models.CharField(max_length=512, verbose_name='Misioni 1 Anglisht')
    goal1_de = models.CharField(max_length=512, verbose_name='Misioni 1 Gjermanisht')
    
    goal2_sq = models.CharField(max_length=512, verbose_name='Missioni 2 Shqip')
    goal2_en = models.CharField(max_length=512, verbose_name='Misioni 2 Anglisht')
    goal2_de = models.CharField(max_length=512, verbose_name='Misioni 2 Gjermanisht')
    
    goal3_sq = models.CharField(max_length=512, verbose_name='Missioni 3 Shqip')
    goal3_en = models.CharField(max_length=512, verbose_name='Misioni 3 Anglisht')
    goal3_de = models.CharField(max_length=512, verbose_name='Misioni 3 Gjermanisht')
    
    goal4_sq = models.CharField(max_length=512, verbose_name='Missioni 4 Shqip')
    goal4_en = models.CharField(max_length=512, verbose_name='Misioni 4 Anglisht')
    goal4_de = models.CharField(max_length=512, verbose_name='Misioni 4 Gjermanisht')
    
    buttonText_sq = models.CharField(max_length=512, verbose_name='Butoni Shqip')
    buttonText_en = models.CharField(max_length=512, verbose_name='Butoni Anglisht')
    buttonText_de = models.CharField(max_length=512, verbose_name='Butoni Gjermanisht')

    class Meta: 
        verbose_name_plural = 'Tech Mission Text te Index Page'

    def __str__(self):
        return f"{self.index}. {self.title_en}"

class HackathonText(models.Model):
    title_sq = models.CharField(max_length=255, verbose_name="Titulli Shqip")
    title_en = models.CharField(max_length=255, verbose_name="Title English")
    title_de = models.CharField(max_length=255, verbose_name="Titel Deutsch")

    description_sq = models.TextField(verbose_name="Përshkrimi Shqip")
    description_en = models.TextField(verbose_name="Description English")
    description_de = models.TextField(verbose_name="Beschreibung Deutsch")

    point1_sq = models.CharField(max_length=512, verbose_name="Pika 1 Shqip")
    point1_en = models.CharField(max_length=512, verbose_name="Point 1 English")
    point1_de = models.CharField(max_length=512, verbose_name="Punkt 1 Deutsch")

    point2_sq = models.CharField(max_length=512, verbose_name="Pika 2 Shqip")
    point2_en = models.CharField(max_length=512, verbose_name="Point 2 English")
    point2_de = models.CharField(max_length=512, verbose_name="Punkt 2 Deutsch")

    point3_sq = models.CharField(max_length=512, verbose_name="Pika 3 Shqip")
    point3_en = models.CharField(max_length=512, verbose_name="Point 3 English")
    point3_de = models.CharField(max_length=512, verbose_name="Punkt 3 Deutsch")

    event_date_sq = models.CharField(max_length=255, verbose_name="Data Shqip")
    event_date_en = models.CharField(max_length=255, verbose_name="Date English")
    event_date_de = models.CharField(max_length=255, verbose_name="Datum Deutsch")

    register_button_sq = models.CharField(max_length=255, verbose_name="Butoni Shqip", default="Regjistrohu Tani")
    register_button_en = models.CharField(max_length=255, verbose_name="Button English", default="Pre-Register Now")
    register_button_de = models.CharField(max_length=255, verbose_name="Button Deutsch", default="Jetzt Vorregistrieren")

    image = models.ImageField(upload_to="hackathon_images/", verbose_name="Imazhi", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Summer Hackathon 2025 Translations"

    def __str__(self):
        return self.title_en



class ContactUs(models.Model):
    name = models.CharField(max_length=512, verbose_name='Emri')
    email = models.EmailField(verbose_name='Emaili')
    subject = models.CharField(max_length=1024, verbose_name='Subjekti')
    message = models.TextField(verbose_name='Mesazhi')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP Address')
    device_name = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Device Name')
    browser_info = models.TextField(null=True, blank=True, verbose_name='Browser Info')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Mesazhet'

    def __str__(self):
        return f"Mesazh nga: {self.name}, subjekti: {self.subject}"
    


class ContactInfo(models.Model):
    address = models.CharField(max_length = 1024, 
            default = "", blank = True, null = True, verbose_name = 'Adresa')

    contact_nr = models.CharField(max_length = 32,
            default = "", blank = True, null = True, verbose_name = 'Numri i kontaktit')

    email = models.EmailField(default = None, blank = True, null = True, verbose_name = 'Emaili')

    facebook_url = models.URLField(default = "", verbose_name = 'Linku i facebookut')
    instagram_url = models.URLField(default = "", verbose_name = 'Linku i instagramit')
    
    class Meta:
        verbose_name_plural = '(7) Infot rreth nesh (te kontaktit)'

    def __str__(self):
        return f"Infot e kontaktit (mos e fshi)"



class ContactText(models.Model):
    title_sq = models.CharField(max_length=255, verbose_name="Titulli Shqip")
    title_en = models.CharField(max_length=255, verbose_name="Title English")
    title_de = models.CharField(max_length=255, verbose_name="Titel Deutsch")

    subtitle_sq = models.TextField(verbose_name="Nëntitulli Shqip")
    subtitle_en = models.TextField(verbose_name="Subtitle English")
    subtitle_de = models.TextField(verbose_name="Untertitel Deutsch")

    connect_sq = models.CharField(max_length=255, verbose_name="Lidhu me Ne Shqip")
    connect_en = models.CharField(max_length=255, verbose_name="Connect With Us English")
    connect_de = models.CharField(max_length=255, verbose_name="Verbinde Dich mit Uns Deutsch")

    description_sq = models.TextField(verbose_name="Përshkrimi Shqip")
    description_en = models.TextField(verbose_name="Description English")
    description_de = models.TextField(verbose_name="Beschreibung Deutsch")

    email_label_sq = models.CharField(max_length=255, verbose_name="Email Label Shqip", default="Email:")
    email_label_en = models.CharField(max_length=255, verbose_name="Email Label English", default="Email:")
    email_label_de = models.CharField(max_length=255, verbose_name="Email Label Deutsch", default="E-Mail:")

    address_label_sq = models.CharField(max_length=255, verbose_name="Adresa Shqip", default="Adresa Kryesore:")
    address_label_en = models.CharField(max_length=255, verbose_name="Address English", default="Main Address:")
    address_label_de = models.CharField(max_length=255, verbose_name="Adresse Deutsch", default="Hauptadresse:")

    form_name_sq = models.CharField(max_length=255, verbose_name="Emri Shqip", default="Emri Juaj")
    form_name_en = models.CharField(max_length=255, verbose_name="Name English", default="Your Name")
    form_name_de = models.CharField(max_length=255, verbose_name="Name Deutsch", default="Ihr Name")

    form_email_sq = models.CharField(max_length=255, verbose_name="Email Shqip", default="Emaili Juaj")
    form_email_en = models.CharField(max_length=255, verbose_name="Email English", default="Your Email")
    form_email_de = models.CharField(max_length=255, verbose_name="Email Deutsch", default="Ihre E-Mail")

    form_subject_sq = models.CharField(max_length=255, verbose_name="Subjekti Shqip", default="Subjekti")
    form_subject_en = models.CharField(max_length=255, verbose_name="Subject English", default="Subject")
    form_subject_de = models.CharField(max_length=255, verbose_name="Betreff Deutsch", default="Betreff")

    form_message_sq = models.CharField(max_length=255, verbose_name="Mesazhi Shqip", default="Mesazhi Juaj")
    form_message_en = models.CharField(max_length=255, verbose_name="Message English", default="Your Message")
    form_message_de = models.CharField(max_length=255, verbose_name="Nachricht Deutsch", default="Ihre Nachricht")

    submit_button_sq = models.CharField(max_length=255, verbose_name="Butoni Shqip", default="Dërgo Mesazh")
    submit_button_en = models.CharField(max_length=255, verbose_name="Button English", default="Send Message")
    submit_button_de = models.CharField(max_length=255, verbose_name="Button Deutsch", default="Nachricht Senden")

    success_message_sq = models.CharField(max_length=255, verbose_name="Mesazhi i Suksesit Shqip", default="Mesazhi juaj është dërguar. Faleminderit!")
    success_message_en = models.CharField(max_length=255, verbose_name="Success Message English", default="Your message has been sent. Thank you!")
    success_message_de = models.CharField(max_length=255, verbose_name="Erfolgsmeldung Deutsch", default="Ihre Nachricht wurde gesendet. Danke!")

    class Meta:
        verbose_name_plural = "Contact Section Translations"

    def __str__(self):
        return self.title_en
    

# FOOTER SECTION
class FooterText(models.Model):
    sitename_sq = models.CharField(max_length=255, verbose_name="Emri i shoqatës")
    sitename_en = models.CharField(max_length=255, verbose_name="Society Name")
    sitename_de = models.CharField(max_length=255, verbose_name="Name der Gesellschaft")

    description_sq = models.TextField(verbose_name="Përshkrimi Shqip")
    description_en = models.TextField(verbose_name="Description English")
    description_de = models.TextField(verbose_name="Beschreibung Deutsch")

    copyright_sq = models.CharField(max_length=255, verbose_name="E drejta e autorit Shqip")
    copyright_en = models.CharField(max_length=255, verbose_name="Copyright English")
    copyright_de = models.CharField(max_length=255, verbose_name="Urheberrecht Deutsch")

    class Meta:
        verbose_name_plural = "Footer Translations"

    def __str__(self):
        return self.sitename_en

