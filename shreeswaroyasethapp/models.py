from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
from django.utils.translation import gettext_lazy as _
import random
import string

date_format = '%Y-%m-%d %H:%M:%S'

class BaseModel(models.Model):
    RECORD_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Deleted', 'Deleted'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)       
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by"
    )
    remark = models.TextField(blank=True, null=True)
    record_status = models.CharField(max_length=20, choices=RECORD_STATUS_CHOICES, default='Active')

    class Meta:
        abstract = True  


def generate_random_string(N):
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    return res
  
def generate_slug(text,modelname):
    new_slug = slugify(text)
    # from home.models import BlogModel

    if modelname.objects.filter(slug=new_slug).exists():
        return generate_slug(text + generate_random_string(5),modelname)
    return new_slug


class UserTypeMaster(BaseModel):
    usertype_id = models.AutoField(primary_key=True)
    usertype_text = models.CharField(max_length=100, blank=False, null=False)
    user_type = models.CharField(max_length=20, blank=False, null=False, unique=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    
    def __str__(self):
        return self.usertype_text

    def userlist(self):
        return UserMaster.objects.filter(user_type=self.user_type, status='1')

    class Meta:
        db_table = "UserTypeMaster"


class AccessTypeMaster(BaseModel):
    accesstype_id = models.AutoField(primary_key=True)
    accesstype_text = models.CharField(max_length=100, blank=False, null=False)
    access_type = models.CharField(max_length=20, blank=False, null=False, unique=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
   

    def __str__(self):
        return self.accesstype_text

    def userlist(self):
        return UserMaster.objects.filter(access_type=self.access_type, status='1')

    class Meta:
        db_table = "AccessTypeMaster"


class UserMaster(BaseModel):
    user_id = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=10, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)

    class Meta:
        db_table = 'UserMaster'

    def __str__(self):
        return self.email
       
        

class UserMasterDetails(BaseModel):
    usermasterdetail_id = models.AutoField(primary_key=True)
    usermaster = models.OneToOneField(to=UserMaster, on_delete=models.PROTECT, blank=True, null=True)
    from_date = models.DateField(auto_now_add=True, blank=True, null=True)
    to_date = models.DateField(default=datetime.strptime('9999-12-31 00:00:00', date_format), blank=True, null=True)
    access_type = models.ForeignKey(to="AccessTypeMaster", to_field="accesstype_id", on_delete=models.PROTECT, null=True)
    user_type = models.ForeignKey(to="UserTypeMaster", to_field="user_type", on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    mobile = models.CharField(max_length=300, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)
    paid_or_free = models.PositiveSmallIntegerField(default=0, blank=True, null=True)  # 0=Free, 1=Paid
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    last_login_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'UserMasterDetails'

    def __str__(self):
        return str(self.usermaster.user_id)
     

BLOG_CATEGORY_CHOICES = [
    ('travel guide', 'Travel Guide'),
    ('adventure', 'Adventure'),
    ('food dining', 'Food & Dining'),
    ('travel tips', 'Travel Tips'),
    ('destinations', 'Destinations'),
]


class BlogPost(BaseModel):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    blog_category = models.CharField(max_length=50, choices=BLOG_CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    image = models.ImageField(upload_to="blogs_pics/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="blogs_banner/", blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    description_1 = models.TextField(blank=True, null=True)
    description_2 = models.TextField(blank=True, null=True)
    description_3 = models.TextField(blank=True, null=True)
    description_4 = models.TextField(blank=True, null=True)

    # 👉 Blog Tags (Many-to-Many)
    content = models.TextField(blank=True, null=True)
    srno = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    psrno = models.PositiveSmallIntegerField(default=999, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title, BlogPost)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
               

class BlogTag(BaseModel):
    
    tag_name = models.CharField(max_length=50, blank=True ,null=True)
    blog = models.ForeignKey(BlogPost, on_delete=models.SET_NULL, null=True, blank=True, related_name="BlogTag")
    
    def __str__(self):
        return self.tag_name


class ContactUs(BaseModel):
    ContactUs_id = models.AutoField(primary_key=True)
    ContactUs_Name = models.CharField(max_length=255,blank=True, null=True)
    ContactUs_description = models.CharField(max_length=255,blank=True, null=True)
    ContactUs_mobile_number_header = models.CharField(max_length=255,blank=True, null=True)
    ContactUs_Emailid_header = models.CharField(max_length=255,blank=True, null=True)
    Working_Hours_header = models.CharField(max_length=255,blank=True, null=True)
    ContactUs_logo = models.ImageField(upload_to="BP", blank=True, null=True)
    ContactUs_Address1_head = models.CharField(max_length=255,blank=True, null=True)
    ContactUs_Address1 = models.TextField(blank=True, null=True)
    ContactUs_Address2_head = models.CharField(max_length=255,blank=True, null=True)
    ContactUs_Address2 = models.TextField(blank=True, null=True)
    ContactUs_EMAIL_ID = models.CharField(max_length=255,blank=True, null=True)
    ContactUs_Mobile_Number_1 = models.CharField(max_length=255,blank=True, null=True)
    ContactUs_Mobile_Number_2 = models.CharField(max_length=255,blank=True, null=True)
    Working_Hours_Time = models.TextField(blank=True, null=True)
    ContactUs_Whatsup_Number = models.CharField(max_length=255,blank=True, null=True)
    Bio = models.TextField(blank=True, null=True)
    Facebook = models.CharField(max_length=300, blank=True, null=True)
    Instagram = models.CharField(max_length=300, blank=True, null=True)
    Linkedin = models.CharField(max_length=300, blank=True, null=True)
    Youtube = models.CharField(max_length=300, blank=True, null=True)
    ContactUs_Form_EMAIL = models.CharField(max_length=300, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    brand_logo = models.ImageField(upload_to="logo", blank=True, null=True)
    footer_description = models.TextField(blank=True , null=True)
    
    class Meta:
        db_table = 'ContactUs'

    def __str__(self):
        return str(self.ContactUs_Name)


class Slider(BaseModel):
    Slider_id = models.AutoField(primary_key=True)
    Slider_topline = models.CharField(max_length=255,blank=True, null=True)
    Slider_maintext = models.CharField(max_length=255,blank=True, null=True)
    Slider_lastline = models.TextField(blank=True, null=True)
    Slider_image1 = models.ImageField(upload_to="Hero_img", blank=True, null=True)
    Slider_image2 = models.ImageField(upload_to="Hero_img", blank=True, null=True)
    Slider_button = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    Slider_button_text = models.CharField(max_length=255,blank=True, null=True)
    Slider_button_link = models.CharField(max_length=255,blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    Sider_srno = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'Slider'

    def __str__(self):
        return "ID - "+ str(self.Slider_id)+" , Top Line - "+ str(self.Slider_topline)+" , Main Text - "+ str(self.Slider_maintext)


class AboutUs(BaseModel):
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Top Line Title")
    )

    full_description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Detailed Description")
    )

    # ---------- NUMERIC STATS ----------
    happy_travelers = models.CharField(max_length=255, blank=True, null=True)
    years_experience = models.CharField(max_length=255, blank=True, null=True)
    uae_branches = models.CharField(max_length=255, blank=True, null=True)
    customer_satisfaction = models.CharField(max_length=255, blank=True, null=True)

    # ---------- MISSION & VISION ----------
    mission_title = models.CharField(max_length=255, blank=True, null=True)
    mission_description = models.TextField(blank=True, null=True)
    vision_title = models.CharField(max_length=255, blank=True, null=True)
    vision_description = models.TextField(blank=True, null=True)

    # ---------- CORE VALUES ----------
    core_values_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Core Values Title"))
    short_description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Core value Short Description")
    )
    value_1_title = models.CharField(max_length=255, blank=True, null=True)
    value_1_description = models.TextField(blank=True, null=True)
    value_2_title = models.CharField(max_length=255, blank=True, null=True)
    value_2_description = models.TextField(blank=True, null=True)
    value_3_title = models.CharField(max_length=255, blank=True, null=True)
    value_3_description = models.TextField(blank=True, null=True)
    value_4_title = models.CharField(max_length=255, blank=True, null=True)
    value_4_description = models.TextField(blank=True, null=True)

    # ---------- IMAGES ----------
    # header_image = models.ImageField(upload_to="about_us/", blank=True, null=True)
    # mission_image = models.ImageField(upload_to="about_us/", blank=True, null=True)
    # vision_image = models.ImageField(upload_to="about_us/", blank=True, null=True)

    # ---------- STATUS ----------
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'about_us'
        verbose_name = "About Us"
        verbose_name_plural = "About Us"
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.title or "About Us Section"
    

class banner(BaseModel):
    image = models.ImageField(upload_to="Banner/", blank=True, null=True)    
    page = models.CharField(max_length=100, blank=True, null=True)
    banner_titile = models.CharField(max_length=150, blank=True, null=True)
    banner_sub_titile = models.CharField(max_length=120, blank=True, null=True)
    

    class Meta:
         db_table = "banner_master"

    def __str__(self):
        return f"{self.page or 'Banner'}"


class FAQ(BaseModel):
    Qus = models.TextField(unique=True)
    Ans = models.TextField()
    Qus_srno = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    
    class Meta:
        db_table = 'FAQ'

    def __str__(self):
        return str(self.Qus)
    

class ContectUsSubmit(BaseModel):
    ContectUs_Submit_id  = models.AutoField(primary_key=True)
    ContectUs_name=models.CharField(max_length=255,blank=True, null=True)
    ContectUs_email=models.CharField(max_length=255,blank=True, null=True)
    ContectUs_cono=models.CharField(max_length=255,blank=True, null=True)
    ContectUs_Destination=models.CharField(max_length=255,blank=True, null=True)
    ContectUs_message=models.CharField(max_length=255,blank=True, null=True)
    ContectUs_Travel_Date = models.DateTimeField(blank=True, null=True)
    ContectUs_Submit_Latitude= models.CharField(max_length=255,blank=True, null=True)
    ContectUs_Submit_Longitude= models.CharField(max_length=255,blank=True, null=True)
    ContectUs_Submit_Date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ContectUs_Submit_Device=models.TextField(blank=True, null=True)
    ContectUs_Submit_Device_ID=models.TextField(blank=True, null=True)
    ContectUs_Submit_IP=models.TextField(blank=True, null=True)
    ContectUs_Submit_Page=models.TextField(blank=True, null=True)
    ContectUs_Submit_OS=models.TextField(blank=True, null=True)
    
    status = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
   

    class Meta:
        db_table = 'ContectUs_Submit'

    def __str__(self):
        return str(self.ContectUs_name) if self.ContectUs_name else str(self.ContectUs_Submit_id)
    


class CityMaster(BaseModel):
    City_id = models.AutoField(primary_key=True)
    thumb_img = models.FileField(upload_to="city_image", blank=True, null=True)
    city_titile = models.CharField(max_length=255, blank=True, null=True)
    city_sort_description = models.CharField(max_length=255,blank=True, null=True)
    city_description_1 = models.TextField(blank=True, null=True)
    city_description_2 = models.TextField(blank=True, null=True)
    city_description_3 = models.TextField(blank=True, null=True)
    city_description_4 = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True ,  unique=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.city_titile:
            from .models import CityMaster
            self.slug = generate_slug(self.city_titile, CityMaster)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'CityMaster'

    def __str__(self):
        return str(self.city_titile)



class Tourmaster(BaseModel):
    TOUR_CATEGORY_CHOICES = [
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('luxury', 'Luxury'),
        ('nature', 'Nature'),
        ('complete', 'Complete'),
        ('category', 'Category'),
        # 🌍 Main Category Types (Tour Nature)
        ('international_tour', 'International Tour'),
        ('domestic_tour', 'Domestic Tour'),
        ('honeymoon_tour', 'Honeymoon Tour'),
        ('family_tour', 'Family Tour'),
        ('group_tour', 'Group Tour'),
        ('luxury_tour', 'Luxury Tour'),
        ('budget_tour', 'Budget Tour'),
        ('corporate_business_tour', 'Corporate / Business Tour'),
        ('student_tour', 'Student Tour'),
        ('custom_tour', 'Custom Tour (Tailor-Made)'),

        # 🏖 Destination-Based Category
        ('dubai_tour', 'Dubai Tour'),
        ('thailand_tour', 'Thailand Tour'),
        ('singapore_tour', 'Singapore Tour'),
        ('malaysia_tour', 'Malaysia Tour'),
        ('bali_tour', 'Bali Tour'),
        ('maldives_tour', 'Maldives Tour'),
        ('europe_tour', 'Europe Tour'),
        ('usa_tour', 'USA Tour'),
        ('australia_tour', 'Australia Tour'),
        ('mauritius_tour', 'Mauritius Tour'),
        ('india_tour', 'India Tour'),
        ('kashmir_tour', 'Kashmir Tour'),
        ('himachal_tour', 'Himachal Tour'),
        ('rajasthan_tour', 'Rajasthan Tour'),
        ('kerala_tour', 'Kerala Tour'),
        ('north_east_india_tour', 'North East India Tour'),
        ('andaman_tour', 'Andaman Tour'),
        ('goa_tour', 'Goa Tour'),
        ('nepal_tour', 'Nepal Tour'),
        ('bhutan_tour', 'Bhutan Tour'),

        # ⏳ Duration-Based Category
        ('2n_3d', '2 Nights / 3 Days'),
        ('3n_4d', '3 Nights / 4 Days'),
        ('4n_5d', '4 Nights / 5 Days'),
        ('5n_6d', '5 Nights / 6 Days'),
        ('6n_7d', '6 Nights / 7 Days'),
        ('7n_8d', '7 Nights / 8 Days'),
        ('8n_9d', '8 Nights / 9 Days'),
        ('9n_10d', '9 Nights / 10 Days'),
        ('10n_plus', '10+ Days Tour'),

        # 🎯 Theme / Experience-Based Category
        ('adventure_tour', 'Adventure Tour'),
        ('beach_holiday', 'Beach Holiday'),
        ('desert_experience', 'Desert Experience'),
        ('wildlife_tour', 'Wildlife Tour'),
        ('hill_station_tour', 'Hill Station Tour'),
        ('religious_pilgrimage_tour', 'Religious / Pilgrimage Tour'),
        ('cruise_experience', 'Cruise Experience'),
        ('romantic_couple_tour', 'Romantic / Couple Tour'),
        ('cultural_heritage_tour', 'Cultural & Heritage Tour'),
        ('shopping_tour', 'Shopping Tour'),
        ('festival_special_tour', 'Festival Special Tour'),
        ('weekend_getaway', 'Weekend Getaway'),
        ('wellness_spa_tour', 'Wellness & Spa Tour'),
        ('short_break', 'Short Break / Mini Holiday'),
        ('educational_tour', 'Educational Tour'),

        # 💼 Package Type (Optional for Backend Use)
        ('fixed_departure', 'Fixed Departure'),
        ('customized_package', 'Customized Package'),
        ('group_departure', 'Group Departure'),
        ('early_bird_offer', 'Early Bird Offer'),
        ('special_discounted_package', 'Special Discounted Package'),
        ('all_inclusive_package', 'All-Inclusive Package'),
        ('visa_flight_hotel_package', 'Visa + Flight + Hotel Package'),
        ('land_only_package', 'Land-Only Package'),
        ('seasonal_offer', 'Seasonal Offer (Summer / Winter)'),
    ]

    CURRENCY_CHOICES = [
        ('INR', 'INR (₹)'),
        ('USD', 'USD ($)'),
        ('EUR', 'EUR (€)'),
        ('GBP', 'GBP (£)'),
    ]

    BASIS_CHOICES = [
        ('per_person', 'Per Person'),
        ('per_day', 'Per Day'),
        ('per_night', 'Per Night'),
        ('per_group', 'Per Group'),
    ]

    Tour_id = models.AutoField(primary_key=True)
    tour_title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    thumb_img = models.FileField(upload_to="Tourpackage", blank=True, null=True)
    banner_img = models.FileField(upload_to="Tourpackagebanner", blank=True, null=True)

    city = models.ForeignKey(CityMaster, on_delete=models.PROTECT, null=True, blank=True , related_name="Tourmaster")
    category = models.CharField(max_length=50, choices=TOUR_CATEGORY_CHOICES, default='adventure', blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True, help_text="Example: '5 Days / 4 Nights'")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='INR', blank=True, null=True)
    on_basis = models.CharField(max_length=50, choices=BASIS_CHOICES, default='per_person', blank=True, null=True)
    package_info = models.TextField(blank=True, null=True)


   
    # Paragraph = models.TextField(blank=True, null=True)
    # extra = models.TextField(blank=True, null=True)
    # button = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    # remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Tourmaster'

    def __str__(self):
        return str(self.tour_title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.tour_title, Tourmaster)
        super(Tourmaster, self).save(*args, **kwargs)



class TourItineraryMaster(BaseModel):
    itinerary_id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(Tourmaster, on_delete=models.CASCADE, related_name="TourItineraryMaster")
    day_number = models.PositiveIntegerField()
    day_heading = models.CharField(max_length=255, blank=True, null=True)
    day_detail = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'TourItineraryMaster'
        ordering = ['day_number']

    def __str__(self):
        return f"{self.tour.tour_title} - Day {self.day_number}"


class TourFacility(BaseModel):
    FACILITY_TYPE_CHOICES = [
        ('included', 'Included'),
        ('excluded', 'Excluded'),
    ]

    facility_id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(Tourmaster, on_delete=models.CASCADE, related_name="TourFacility")
    facility_name = models.CharField(max_length=255, blank=True, null=True)
    include_exclude = models.CharField(max_length=20, choices=FACILITY_TYPE_CHOICES, default='included')

    class Meta:
        db_table = 'TourFacility'

    def __str__(self):
        return f"{self.facility_name} ({self.include_exclude})"


class TourSpecificationMaster(BaseModel):
    spec_id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(Tourmaster, on_delete=models.CASCADE, related_name="TourSpecificationMaster")
    specification_name = models.CharField(max_length=255, blank=True, null=True)
    specification_value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'TourSpecificationMaster'

    def __str__(self):
        return f"{self.specification_name}: {self.specification_value}"


class TourRatingMaster(BaseModel):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating_id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(Tourmaster, on_delete=models.CASCADE, related_name="TourRatingMaster")
    user = models.ForeignKey( UserMaster , on_delete=models.CASCADE , blank=True, null=True)

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    title = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "TourRatingMaster"
        ordering = ['-created_at']
        verbose_name = "Tour Rating"
        verbose_name_plural = "Tour Ratings"

    def __str__(self):
        return f"{self.tour.tour_title} - {self.rating}⭐"


class ServiceMaster(BaseModel):
    Service_id = models.AutoField(primary_key=True)
    service_title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    # city = models.ForeignKey(CityMaster, on_delete=models.CASCADE, null=True, blank=True, related_name="services")
    image = models.FileField(upload_to="Service/", blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=255,blank=True, null=True)
    
    # Home Page Feature Highlights
    service_home_feature_1 = models.CharField(max_length=255, blank=True, null=True)
    service_home_feature_2 = models.CharField(max_length=255, blank=True, null=True)
    service_home_feature_3 = models.CharField(max_length=255, blank=True, null=True)
    service_home_feature_4 = models.CharField(max_length=255, blank=True, null=True)
    is_home = models.BooleanField(default=False)

    class Meta:
        db_table = "ServiceMaster"
        verbose_name = "Service Master"
        verbose_name_plural = "Service Masters"
        indexes = [
            # models.Index(fields=['city']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return str(self.service_title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.service_title, ServiceMaster)
        super(ServiceMaster, self).save(*args, **kwargs)


class ServiceFeature(BaseModel):
    feature_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(ServiceMaster, on_delete=models.CASCADE, related_name="ServiceFeature")
    feature_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "ServiceFeature"
        verbose_name = "Service Feature"
        verbose_name_plural = "Service Features"

    def __str__(self):
        return f"{self.service.service_title} - {self.feature_name}"


# ✅ Service Details (Sequential)
class ServiceDetailMaster(BaseModel):
    detail_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(ServiceMaster, on_delete=models.CASCADE, related_name="ServiceDetailMaster")
    seq_no = models.PositiveSmallIntegerField(default=1)
    detail_text = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "ServiceDetailMaster"
        verbose_name = "Service Detail"
        verbose_name_plural = "Service Details"
        ordering = ['seq_no']

    def __str__(self):
        return f"{self.service.service_title} - Detail {self.seq_no}"


class ServiceHighlightMaster(BaseModel):
    highlight_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(ServiceMaster, on_delete=models.CASCADE, related_name="ServiceHighlightMaster")
    service_highlight = models.CharField(max_length=255, blank=True, null=True)
    service_highlight_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "ServiceHighlightMaster"
        verbose_name = "Service Highlight"
        verbose_name_plural = "Service Highlights"

    def __str__(self):
        return f"{self.service_highlight} - {self.service.service_title}"



class HotelMaster(BaseModel):
    CURRENCY_CHOICES = [
        ('INR', 'INR (₹)'),
        ('USD', 'USD ($)'),
        ('EUR', 'EUR (€)'),
    ]
    BASIS_CHOICES = [
        ('per person', 'Per Person'),
        ('per day', 'Per Day'),
        ('per night', 'Per Night'),
        ('per group', 'Per Group'),
    ]

    hotel_id = models.AutoField(primary_key=True)
    hotel_title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    city = models.ForeignKey('CityMaster', on_delete=models.PROTECT, null=True, blank=True, related_name="hotels")
    address = models.CharField(max_length=255, blank=True, null=True)
    star_rating = models.PositiveSmallIntegerField(default=5)
    total_reviews = models.PositiveIntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='INR')
    on_basis = models.CharField(max_length=50, choices=BASIS_CHOICES, default='per_night')
    thumbnail = models.FileField(upload_to="hotel/thumbs", blank=True, null=True)
    banner_image = models.FileField(upload_to="hotel/banner", blank=True, null=True)

    short_description = models.TextField(blank=True, null=True)
    about_hotel = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "HotelMaster"
        indexes = [models.Index(fields=["city", "hotel_title"])]

    def __str__(self):
        return str(self.hotel_title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.hotel_title, HotelMaster)
        super().save(*args, **kwargs)


class HotelHighlight(BaseModel):
    highlight_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelMaster, on_delete=models.CASCADE, related_name="HotelHighlight")
    highlight_title = models.CharField(max_length=255, blank=True, null=True)
    highlight_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "HotelHighlight"

    def __str__(self):
        return f"{self.hotel.hotel_title} - {self.highlight_title}"


class HotelAmenity(BaseModel):
    amenity_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelMaster, on_delete=models.CASCADE, related_name="HotelAmenity")
    name = models.CharField(max_length=255, blank=True, null=True)
    icon_class = models.CharField(max_length=100, blank=True, null=True, help_text="FontAwesome icon name")

    class Meta:
        db_table = "HotelAmenity"

    def __str__(self):
        return f"{self.name}"



class HotelRoomType(BaseModel):
    BASIS_CHOICES = [
        ('per person', 'Per Person'),
        ('per day', 'Per Day'),
        ('per night', 'Per Night'),
        ('per group', 'Per Group'),
    ]
    CURRENCY_CHOICES = [
        ('INR', 'INR (₹)'),
        ('USD', 'USD ($)'),
        ('EUR', 'EUR (€)'),
    ]
    room_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelMaster, on_delete=models.CASCADE, related_name="HotelRoomType")
    room_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    on_basis = models.CharField(max_length=50, choices=BASIS_CHOICES, default='per_night')
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='INR')


    class Meta:
        db_table = "HotelRoomType"

    def __str__(self):
        return f"{self.room_name} - {self.hotel.hotel_title}"


class HotelRoomTypefeatures(BaseModel):
    hotelroomtype = models.ForeignKey(HotelRoomType, on_delete=models.CASCADE, related_name="HotelRoomTypefeatures")
    features= models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = "HotelRoomTypefeatures"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.hotelroomtype} - {self.features}"



class HotelRating(BaseModel):
    rating_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelMaster, on_delete=models.CASCADE, related_name="HotelRating")
    user = models.ForeignKey(UserMaster, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "HotelRating"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.hotel.hotel_title} - {self.rating}⭐"



class Testimonial(BaseModel):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    testimonial_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    # country = models.CharField(max_length=100, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    message = models.TextField(help_text="Customer feedback or testimonial message")
    profile_image = models.ImageField(upload_to="testimonials", blank=True, null=True)

    class Meta:
        db_table = "Testimonial"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.rating}★)"



class WhyChooseUs(BaseModel):
    title = models.CharField(max_length=200, help_text="Main section title (e.g. Why Choose Us?)")
    description = models.TextField(help_text="Short paragraph explaining the section")

    def __str__(self):
        return self.title


class WhyChooseUsFeature(BaseModel):
    section = models.ForeignKey(WhyChooseUs, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100, help_text="Feature title (e.g. Licensed & Certified)")

    def __str__(self):
        return self.name
    

