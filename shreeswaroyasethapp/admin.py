from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

# admin.register(Banner)

admin.site.register(UserMaster)
admin.site.register(AccessTypeMaster)
admin.site.register(UserTypeMaster)
admin.site.register(UserMasterDetails)
admin.site.register(BlogTag)
admin.site.register(Slider)

admin.site.register(banner)
admin.site.register(FAQ)
admin.site.register(ContectUsSubmit)
admin.site.register(Tourmaster)
admin.site.register(TourItineraryMaster)
admin.site.register(TourFacility)
admin.site.register(TourSpecificationMaster)
admin.site.register(TourRatingMaster)
admin.site.register(ServiceFeature)
admin.site.register(HotelAmenity)
admin.site.register(HotelRoomType)
admin.site.register(HotelRating)
admin.site.register(Testimonial)
admin.site.register(HotelRoomTypefeatures)
admin.site.register(WhyChooseUsFeature)


@admin.register(BlogPost)
class BlogPostsAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'description_1',
        'description_2',
        'description_3',
        'description_4',
        'content',      
    )

@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'description',
        
    )
    
@admin.register(ContactUs)
class contactAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'footer_description'
    )
    
@admin.register(CityMaster)
class CitymasterAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'city_description_1',
        'city_description_2',
        'city_description_3',
        'city_description_4',
    )

@admin.register(AboutUs)
class AboutUsAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'short_description',
        'full_description',
        
    )
@admin.register(ServiceMaster)
class ServiceMasterAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'short_description',      
    )
@admin.register(ServiceDetailMaster)
class ServiceDetailMasterAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'detail_text',      
    )
@admin.register(ServiceHighlightMaster)
class ServiceHighlightMasterAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'service_highlight_description',      
    )
@admin.register(HotelMaster)
class HotelMasterAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'short_description',  
        'about_hotel'    
    )
@admin.register(HotelHighlight)
class HotelHighlightAdmin(SummernoteModelAdmin):
    summernote_fields = (
        'highlight_description'    
    )



# class BannerAdmin(admin.ModelAdmin):
#     list_display = ('title', 'is_active', 'created_at')  
#     search_fields = ('title',)                            
#     list_filter = ('is_active',)                          
