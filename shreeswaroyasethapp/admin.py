from django.contrib import admin
from .models import *
import nested_admin
from django_summernote.admin import SummernoteModelAdmin , SummernoteInlineModelAdmin

# admin.register(Banner)

admin.site.register(UserMaster)
admin.site.register(AccessTypeMaster)
admin.site.register(UserTypeMaster)
admin.site.register(UserMasterDetails)
admin.site.register(Slider)

admin.site.register(banner)
admin.site.register(FAQ)
admin.site.register(ContectUsSubmit)
admin.site.register(WhyChooseUsFeature)
admin.site.register(Testimonial)

# admin.site.register(Tourmaster)
# admin.site.register(TourItineraryMaster)
# admin.site.register(TourFacility)
# admin.site.register(TourSpecificationMaster)
# admin.site.register(TourRatingMaster)

# ------------- INLINE CLASSES ------------- #

class TourItineraryInline(SummernoteInlineModelAdmin, nested_admin.NestedStackedInline):
    """Day-wise itinerary"""
    model = TourItineraryMaster
    extra = 1
    classes = ['collapse']


class TourFacilityInline(nested_admin.NestedStackedInline):
    """Facilities included in the tour"""
    model = TourFacility
    extra = 1
    classes = ['collapse']


class TourSpecificationInline(nested_admin.NestedStackedInline):
    """Specifications or inclusions/exclusions"""
    model = TourSpecificationMaster
    extra = 1
    classes = ['collapse']



class TourRatingInline(nested_admin.NestedStackedInline):
    """User ratings and reviews (read-only)"""
    model = TourRatingMaster
    extra = 0
    classes = ['collapse']
    # readonly_fields = ('user', 'rating', 'review_text', 'created_at')


# ------------- MAIN ADMIN CLASS ------------- #

@admin.register(Tourmaster)
class TourMasterAdmin(SummernoteModelAdmin, nested_admin.NestedModelAdmin):
    summernote_fields = ('package_info',)
    inlines = [
        TourItineraryInline,
        TourFacilityInline,
        TourSpecificationInline,
        TourRatingInline,
    ]
    # list_display = ('tour_title', 'city', 'price', 'currency', 'days')
    # search_fields = ('tour_title', 'city__city_titile')
    # list_filter = ('city', 'currency')




class BlogTagInline(nested_admin.NestedStackedInline):
    """Tags under each blog post"""
    model = BlogTag
    extra = 1
    classes = ['collapse']

    
@admin.register(BlogPost)
class BlogPostsAdmin(SummernoteModelAdmin, nested_admin.NestedModelAdmin):
    summernote_fields = (
        'description_1',
        'description_2',
        'description_3',
        'description_4',
        'content',
    )
    inlines = [BlogTagInline]
    list_display = ('title', 'created_at', 'author')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)



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



admin.site.register(ServiceFeature)

class ServiceFeatureInline(nested_admin.NestedStackedInline):
    """Inline for features"""
    model = ServiceFeature
    extra = 1
    classes = ['collapse']
    


class ServiceDetailInline(SummernoteInlineModelAdmin, nested_admin.NestedStackedInline):
    """Inline for service details"""
    model = ServiceDetailMaster
    summernote_fields = ('detail_text',)
    extra = 1
    classes = ['collapse']


class ServiceHighlightInline(SummernoteInlineModelAdmin, nested_admin.NestedStackedInline):
    """Inline for service highlights"""
    model = ServiceHighlightMaster
    summernote_fields = ('service_highlight_description',)
    extra = 1
    classes = ['collapse']

# ---- MAIN ADMIN ---- #

@admin.register(ServiceMaster)
class ServiceMasterAdmin(SummernoteModelAdmin, nested_admin.NestedModelAdmin):
    summernote_fields = ('short_description',)
    inlines = [
        ServiceDetailInline,
        ServiceHighlightInline,
        ServiceFeatureInline,
    ]

# @admin.register(HotelMaster)
# class HotelMasterAdmin(SummernoteModelAdmin):
#     summernote_fields = (
#         'short_description',  
#         'about_hotel'    
#     )
# @admin.register(HotelHighlight)
# class HotelHighlightAdmin(SummernoteModelAdmin):
#     summernote_fields = (
#         'highlight_description'    
#     )


class HotelRoomTypefeaturesInline(nested_admin.NestedStackedInline):
    """Features under each Room Type"""
    model = HotelRoomTypefeatures
    extra = 1
    classes = ['collapse']


class HotelRoomTypeInline(nested_admin.NestedStackedInline):
    """Room Types under Hotel"""
    model = HotelRoomType
    inlines = [HotelRoomTypefeaturesInline]  # ✅ nested inline
    extra = 1
    classes = ['collapse']


class HotelAmenityInline(nested_admin.NestedStackedInline):
    """Amenities under Hotel"""
    model = HotelAmenity
    extra = 1
    classes = ['collapse']


class HotelHighlightInline(SummernoteInlineModelAdmin,nested_admin.NestedStackedInline):
    model = HotelHighlight
    summernote_fields = ('highlight_description',)  # ✅ summernote active
    extra = 1
    classes = ['collapse']


class HotelRatingInline(nested_admin.NestedStackedInline):
    """Ratings under Hotel"""
    model = HotelRating
    extra = 0
    classes = ['collapse']
    readonly_fields = ('user', 'rating', 'review_text', 'created_at')  # optional


# ---------------------------------------------------
# Combine all in HotelMaster admin
# ---------------------------------------------------
@admin.register(HotelMaster)
class HotelMasterAdmin(SummernoteModelAdmin, nested_admin.NestedModelAdmin):
    summernote_fields = ('short_description', 'about_hotel')
    inlines = [
        HotelHighlightInline,
        HotelAmenityInline,
        HotelRoomTypeInline,
        HotelRatingInline,
    ]
    list_display = ('hotel_title', 'city', 'star_rating', 'price', 'currency')
    search_fields = ('hotel_title', 'city__city_titile')
    list_filter = ('city', 'star_rating', 'currency')         






