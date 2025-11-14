from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ['id', 'created_at', 'updated_at', 'record_status' , 'remark']


class SliderSerializer(BaseModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'        


class AboutUsSerializer(BaseModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'     


class CityMasterSerializer(BaseModelSerializer):
    class Meta:
        model = CityMaster
        fields = '__all__'        


class ContactUsSerializer(serializers.ModelSerializer):
    call_link_1 = serializers.SerializerMethodField()
    call_link_2 = serializers.SerializerMethodField()
    whatsapp_link = serializers.SerializerMethodField()

    class Meta:
        model = ContactUs
        fields = "__all__"
        extra_fields = ["call_link_1", "call_link_2", "whatsapp_link"]

    def get_call_link_1(self, obj):
        """पहले मोबाइल नंबर के लिए tel लिंक"""
        if obj.ContactUs_Mobile_Number_1:
            num = obj.ContactUs_Mobile_Number_1.replace(" ", "").replace("+", "")
            return f"tel:+{num}"
        return None

    def get_call_link_2(self, obj):
        """दूसरे मोबाइल नंबर के लिए tel लिंक"""
        if obj.ContactUs_Mobile_Number_2:
            num = obj.ContactUs_Mobile_Number_2.replace(" ", "").replace("+", "")
            return f"tel:+{num}"
        return None

    def get_whatsapp_link(self, obj):
        """WhatsApp लिंक"""
        if obj.ContactUs_Whatsup_Number:
            num = obj.ContactUs_Whatsup_Number.replace(" ", "").replace("+", "")
            return f"https://wa.me/{num}"
        return None        
    

class FAQSerializer(BaseModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'      

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityMaster
        fields = ['City_id', 'city_titile', 'slug', 'thumb_img']


class TourItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourItineraryMaster
        fields = ['day_number', 'day_heading', 'day_detail']


class TourFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourFacility
        fields = ['facility_name', 'include_exclude']


class TourSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourSpecificationMaster
        fields = ['specification_name', 'specification_value']


class TourRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TourRatingMaster
        fields = ['user_name', 'rating', 'title', 'comment', 'created_at']


class TourDetailSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)  
    itineraries = TourItinerarySerializer(source='TourItineraryMaster', many=True, read_only=True)
    # facilities = TourFacilitySerializer(source='TourFacility', many=True, read_only=True)
    specifications = TourSpecificationSerializer(source='TourSpecificationMaster', many=True, read_only=True)
    ratings = TourRatingSerializer(source='TourRatingMaster', many=True, read_only=True)

    included_facilities = serializers.SerializerMethodField()
    excluded_facilities = serializers.SerializerMethodField()
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)

    class Meta:
        model = Tourmaster
        fields = '__all__'  
        extra_fields = ['included_facilities', 'excluded_facilities']

    def get_included_facilities(self, obj):
        facilities = obj.TourFacility.filter(include_exclude='included')
        return TourFacilitySerializer(facilities, many=True).data

    def get_excluded_facilities(self, obj):
        facilities = obj.TourFacility.filter(include_exclude='excluded')
        return TourFacilitySerializer(facilities, many=True).data

    class Meta:
        model = Tourmaster
        fields = '__all__'


class TestimonialSerializer(BaseModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'            



class BlogTagSerializer(BaseModelSerializer):
    class Meta:
        model = BlogTag
        fields = ['tag_name','id']


class BlogPostSerializer(BaseModelSerializer):
    Tags = BlogTagSerializer(source='BlogTag', many=True, read_only=True)
    author = UserSerializer(read_only=True)
    class Meta:
        model = BlogPost
        fields = '__all__'          


class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeature
        fields = ["feature_id", "feature_name"]


class ServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDetailMaster
        fields = ["detail_id", "seq_no", "detail_text"]


class ServiceHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceHighlightMaster
        fields = ["highlight_id", "service_highlight", "service_highlight_description"]


class ServiceMasterSerializer(serializers.ModelSerializer):
    ServiceFeatures = ServiceFeatureSerializer(source='ServiceFeature', many=True, read_only=True)
    ServiceDetailMasters = ServiceDetailSerializer(source='ServiceDetailMaster' , many=True, read_only=True)
    ServiceHighlightMasters = ServiceHighlightSerializer(source='ServiceHighlightMaster', many=True, read_only=True)

    class Meta:
        model = ServiceMaster
        fields =  '__all__'


class HotelHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelHighlight
        fields = ['highlight_id', 'highlight_title', 'highlight_description']


class HotelAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenity
        fields = ['amenity_id', 'name', 'icon_class']

class HotelRoomTypefeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoomTypefeatures
        fields = ['hotelroomtype' , 'features']


class HotelRoomTypeSerializer(serializers.ModelSerializer):
    RoomTypefeature = HotelRoomTypefeaturesSerializer(source="HotelRoomTypefeatures", many=True, read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    class Meta:
        model = HotelRoomType
        fields = '__all__'


class HotelRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', default=None)

    class Meta:
        model = HotelRating
        fields = ['rating_id', 'user_name', 'rating', 'review_text', 'created_at']


class HotelMasterSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)  
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    
    HotelHighlights = HotelHighlightSerializer(source="HotelHighlight", many=True, read_only=True)
    HotelAmenitys = HotelAmenitySerializer(source="HotelAmenity",many=True, read_only=True)
    HotelRoomTypes = HotelRoomTypeSerializer(source="HotelRoomType",many=True, read_only=True)
    HotelRatings = HotelRatingSerializer( source="HotelRating",many=True, read_only=True)

    class Meta:
        model = HotelMaster
        fields = '__all__'

class WhyChooseUsFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseUsFeature
        fields = ['id', 'name',]

class WhyChooseUsSerializer(serializers.ModelSerializer):
    features = WhyChooseUsFeatureSerializer(many=True, read_only=True)
    
    class Meta:
        model = WhyChooseUs
        fields = '__all__'       

class ContectUsSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContectUsSubmit
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = banner
        fields = '__all__'

class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = '__all__'