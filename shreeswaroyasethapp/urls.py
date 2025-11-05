from django.conf import settings               
from django.conf.urls.static import static      
from django.urls import path
from .views import *  

urlpatterns = [

    path('slider/', SliderAPIView.as_view(), name='Slider'),
    path('slider/<int:pk>/', SliderAPIView.as_view(), name='Slider'),

    path('aboutus/', AboutUsAPIView.as_view(), name='about-us'),
    path('aboutus/<int:pk>/', AboutUsAPIView.as_view(), name='about-us'),

    path('city/', CityMasterAPIView.as_view(), name='city-list-create'),
    path('city/<slug:slug>/', CityMasterAPIView.as_view(), name='city-detail'),

    path('contactus/', ContactUsAPIView.as_view(), name='contact-us'),
    path('contactus/<int:pk>/', ContactUsAPIView.as_view(), name='contact-us'),

    path('faq/', FAQAPIView.as_view(), name='faq'),
    path('faq/<int:pk>/', FAQAPIView.as_view(), name='faq'),

    path('tour/', TourView.as_view(), name='tour-list-create'),         
    path('tour/<int:pk>/', TourView.as_view(), name='tour-detail'),

    path('testimonial/', TestimonialAPIView.as_view(), name='review'),
    
    path('blogpost/', BlogPostAPIView.as_view(), name='blogpost'),         
    path('blogpost/<int:pk>/', BlogPostAPIView.as_view(), name='blogpost-detail'), 

    path("services/", ServiceAPIView.as_view(), name="service-list"),
    path("services/<int:pk>/", ServiceAPIView.as_view(), name="service-detail"),
    
    path("hotel/", HotelAPIView.as_view(), name="hotel-list-create"),
    path("hotel/<int:pk>/", HotelAPIView.as_view(), name="hotel-detail"),

    path('whyChooseUs/', WhyChooseUsView.as_view(), name='whyChooseUs'),         
    path('whyChooseUs/<int:pk>/', WhyChooseUsView.as_view(), name='whyChooseUs-detail'),

    path('contactsubmit/', ContectUsSubmitAPIView.as_view(), name='contact-submit'),
    path('contactsubmit/<int:pk>/', ContectUsSubmitAPIView.as_view(), name='contact-submit'),

    path('banner/', BannerView.as_view(), name='banner-api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
