from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import DatabaseError
from rest_framework.exceptions import ValidationError
from .models import *
from .serializers import *
from shreeswaroyasethapp.models import *
from shreeswaroyasethapp.serializers import *
from django.core.mail import EmailMessage


class SliderAPIView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                obj = get_object_or_404(Slider, pk=pk, record_status="Active")
                serializer = SliderSerializer(obj)
                return Response({
                    "message": "Record fetched successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            objs = Slider.objects.filter(record_status="Active")
            serializer = SliderSerializer(objs, many=True)
            return Response({
                "message": "All active records fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error while fetching records",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = SliderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "Record created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response({
                "message": "Validation failed",
                "errors": ve.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({
                "message": "Database error occurred while saving"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            obj = get_object_or_404(Slider, pk=pk, record_status="Active")
            serializer = SliderSerializer(obj, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "Record updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except ValidationError as ve:
            return Response({
                "message": "Validation failed",
                "errors": ve.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({
                "message": "Database error occurred while updating"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            obj = get_object_or_404(Slider, pk=pk, record_status="Active")
            obj.record_status = "Deleted"
            obj.save()
            return Response({
                "message": "Record marked as Deleted"
            }, status=status.HTTP_200_OK)

        except DatabaseError:
            return Response({
                "message": "Database error occurred while deleting"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AboutUsAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            obj = get_object_or_404(AboutUs, pk=pk, record_status="Active")
            serializer = AboutUsSerializer(obj)
            return Response({"message": "Record fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        objs = AboutUs.objects.filter(record_status="Active")
        serializer = AboutUsSerializer(objs, many=True)
        return Response({"message": "All active records fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AboutUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Record created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to create record", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = get_object_or_404(AboutUs, pk=pk, record_status="Active")
        serializer = AboutUsSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Record updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Failed to update record", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(AboutUs, pk=pk, record_status="Active")
        obj.record_status = "Deleted"
        obj.save()
        return Response({"message": "Record marked as Deleted"}, status=status.HTTP_200_OK)      


class CityMasterAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        city_id = request.query_params.get("id")
        slug = request.query_params.get("slug")

        if city_id:
            city = get_object_or_404(CityMaster, City_id=city_id)
            serializer = CityMasterSerializer(city)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif slug:
            city = get_object_or_404(CityMaster, slug=slug)
            serializer = CityMasterSerializer(city)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            cities = CityMaster.objects.all().order_by('-City_id')
            serializer = CityMasterSerializer(cities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CityMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        city_id = request.data.get("City_id")
        city = get_object_or_404(CityMaster, City_id=city_id)
        serializer = CityMasterSerializer(city, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        city_id = request.query_params.get("id")
        if not city_id:
            return Response({"error": "City_id is required to delete"}, status=status.HTTP_400_BAD_REQUEST)
        city = get_object_or_404(CityMaster, City_id=city_id)
        city.delete()
        return Response({"message": "City deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ContactUsAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            obj = get_object_or_404(ContactUs, pk=pk, record_status="Active")
            serializer = ContactUsSerializer(obj)
            return Response({"message": "Record fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        objs = ContactUs.objects.filter(record_status="Active")
        serializer = ContactUsSerializer(objs, many=True)
        return Response({"message": "All active records fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Record created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Failed to create record", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = get_object_or_404(ContactUs, pk=pk, record_status="Active")
        serializer = ContactUsSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Record updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Failed to update record", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(ContactUs, pk=pk, record_status="Active")
        obj.record_status = "Deleted"
        obj.save()
        return Response({"message": "Record marked as Deleted"}, status=status.HTTP_200_OK)


class FAQAPIView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                obj = get_object_or_404(FAQ, pk=pk, record_status="Active")
                serializer = FAQSerializer(obj)
                return Response({
                    "message": "Record fetched successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            objs = FAQ.objects.filter(record_status="Active")
            serializer = FAQSerializer(objs, many=True)
            return Response({
                "message": "All active records fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error while fetching records",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = FAQSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "Record created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response({
                "message": "Validation failed",
                "errors": ve.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({
                "message": "Database error occurred while saving"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            obj = get_object_or_404(FAQ, pk=pk, record_status="Active")
            serializer = FAQSerializer(obj, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "Record updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except ValidationError as ve:
            return Response({
                "message": "Validation failed",
                "errors": ve.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({
                "message": "Database error occurred while updating"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            obj = get_object_or_404(FAQ, pk=pk, record_status="Active")
            obj.record_status = "Deleted"
            obj.save()
            return Response({
                "message": "Record marked as Deleted"
            }, status=status.HTTP_200_OK)

        except DatabaseError:
            return Response({
                "message": "Database error occurred while deleting"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TourView(APIView):
   
    # ✅ GET — Retrieve single or all tours
    def get(self, request, pk=None):
        slug = request.query_params.get("slug")

        if slug:
            tour = get_object_or_404(Tourmaster, slug=slug)
            serializer = TourDetailSerializer(tour)
        elif pk:
            tour = get_object_or_404(Tourmaster, pk=pk)
            serializer = TourDetailSerializer(tour)
        else:
            tours = Tourmaster.objects.all()
            serializer = TourDetailSerializer(tours, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # ✅ POST — Create a new tour
    def post(self, request):
        serializer = TourDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✅ PUT — Update by pk or slug
    def put(self, request, pk=None):
        slug = request.query_params.get("slug")

        if slug:
            tour = get_object_or_404(Tourmaster, slug=slug)
        elif pk:
            tour = get_object_or_404(Tourmaster, pk=pk)
        else:
            return Response({"error": "Please provide pk or slug"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TourDetailSerializer(tour, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✅ DELETE — Delete by pk or slug
    def delete(self, request, pk=None):
        slug = request.query_params.get("slug")

        if slug:
            tour = get_object_or_404(Tourmaster, slug=slug)
        elif pk:
            tour = get_object_or_404(Tourmaster, pk=pk)
        else:
            return Response({"error": "Please provide pk or slug"}, status=status.HTTP_400_BAD_REQUEST)

        tour.delete()
        return Response({"message": "Tour deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class TestimonialAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            obj = get_object_or_404(Testimonial, pk=pk, record_status="Active")
            serializer = TestimonialSerializer(obj)
            return Response({"message": "Record fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        objs = Testimonial.objects.filter(record_status="Active")
        serializer = TestimonialSerializer(objs, many=True)
        return Response({"message": "All active records fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)   
    

class BlogPostAPIView(APIView):
    def get(self, request, pk=None):
        slug = request.query_params.get("slug")

        try:
            if slug:
                blog = get_object_or_404(BlogPost, slug=slug)
                serializer = BlogPostSerializer(blog)
            elif pk:
                blog = get_object_or_404(BlogPost, pk=pk)
                serializer = BlogPostSerializer(blog)
            else:
                blogs = BlogPost.objects.all()
                serializer = BlogPostSerializer(blogs, many=True)

            return Response({
                "message": "Blog fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error fetching blog data",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ServiceAPIView(APIView):
    def get(self, request, pk=None):
        slug = request.query_params.get("slug") 

        try:
            if slug:
                Service = get_object_or_404(ServiceMaster, slug=slug)
                serializer = ServiceMasterSerializer(Service)
            elif pk:
                Service = get_object_or_404(ServiceMaster, pk=pk)
                serializer = ServiceMasterSerializer(Service)
            else:
                Services = ServiceMaster.objects.all()
                serializer = ServiceMasterSerializer(Services, many=True)

            return Response({
                "message": "Service fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error fetching Service  data",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        

class HotelAPIView(APIView):
    """
    Handles HotelMaster CRUD and detail view (by slug or ID).
    """

    def get_queryset(self):
        """Helper to prefetch all related data for better performance."""
        return HotelMaster.objects.prefetch_related(
            "HotelHighlight", "HotelAmenity", "HotelRoomType", "HotelRating"
        )

    # ✅ GET — Fetch hotels (all / by slug / by id)
    def get(self, request, pk=None):
        slug = request.query_params.get("slug")

        try:
            queryset = self.get_queryset()

            # Fetch by slug
            if slug:
                hotel = get_object_or_404(queryset, slug=slug)
                serializer = HotelMasterSerializer(hotel)
                return Response(
                    {"message": "Hotel fetched successfully", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )

            # Fetch by id
            elif pk:
                hotel = get_object_or_404(queryset, pk=pk)
                serializer = HotelMasterSerializer(hotel)
                return Response(
                    {"message": "Hotel fetched successfully", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )

            # Fetch all hotels
            hotels = queryset.order_by("-created_at")
            serializer = HotelMasterSerializer(hotels, many=True)
            return Response(
                {"message": "All hotels fetched successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": "Error fetching hotel data", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # ✅ POST — Create new hotel
    def post(self, request):
        try:
            serializer = HotelMasterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Hotel created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as ve:
            return Response(
                {"message": "Validation failed", "errors": ve.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DatabaseError:
            return Response(
                {"message": "Database error occurred while saving"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"message": "Unexpected error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # ✅ PUT — Update existing hotel by slug or pk
    def put(self, request, pk=None):
        slug = request.query_params.get("slug")

        try:
            queryset = self.get_queryset()

            if slug:
                hotel = get_object_or_404(queryset, slug=slug)
            elif pk:
                hotel = get_object_or_404(queryset, pk=pk)
            else:
                return Response(
                    {"message": "Please provide slug or id to update"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = HotelMasterSerializer(hotel, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Hotel updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except ValidationError as ve:
            return Response(
                {"message": "Validation failed", "errors": ve.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DatabaseError:
            return Response(
                {"message": "Database error occurred while updating"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"message": "Unexpected error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # ✅ DELETE — Delete hotel by slug or pk
    def delete(self, request, pk=None):
        slug = request.query_params.get("slug")

        try:
            if slug:
                hotel = get_object_or_404(HotelMaster, slug=slug)
            elif pk:
                hotel = get_object_or_404(HotelMaster, pk=pk)
            else:
                return Response(
                    {"message": "Please provide slug or id to delete"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            hotel.delete()
            return Response(
                {"message": "Hotel deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except DatabaseError:
            return Response(
                {"message": "Database error occurred while deleting"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"message": "Unexpected error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )      


class WhyChooseUsView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                obj = get_object_or_404(WhyChooseUs, pk=pk, record_status="Active")
                serializer = WhyChooseUsSerializer(obj)
                return Response({
                    "message": "Record fetched successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            objs = WhyChooseUs.objects.filter(record_status="Active")
            serializer = WhyChooseUsSerializer(objs, many=True)
            return Response({
                "message": "All active records fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error while fetching records",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = WhyChooseUsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "Record created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response({
                "message": "Validation failed",
                "errors": ve.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({
                "message": "Database error occurred while saving"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            obj = get_object_or_404(WhyChooseUs, pk=pk, record_status="Active")
            serializer = WhyChooseUsSerializer(obj, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "Record updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except ValidationError as ve:
            return Response({
                "message": "Validation failed",
                "errors": ve.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({
                "message": "Database error occurred while updating"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            obj = get_object_or_404(WhyChooseUs, pk=pk, record_status="Active")
            obj.record_status = "Deleted"
            obj.save()
            return Response({
                "message": "Record marked as Deleted"
            }, status=status.HTTP_200_OK)

        except DatabaseError:
            return Response({
                "message": "Database error occurred while deleting"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "message": "Unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class ContectUsSubmitAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            obj = get_object_or_404(ContectUsSubmit, pk=pk, record_status="Active")
            serializer = ContectUsSubmitSerializer(obj)
            return Response({"message": "Record fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        objs = ContectUsSubmit.objects.filter(record_status="Active")
        serializer = ContectUsSubmitSerializer(objs, many=True)
        return Response({"message": "All active records fetched successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = ContectUsSubmitSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Record created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response({"message": "Failed to create record", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     serializer = ContectUsSubmitSerializer(data=request.data)
    #     if serializer.is_valid():
    #         instance = serializer.save()

            
    #         subject = "New Contact Us Submission"
    #         message = f"""
    #         You have received a new contact form submission:

    #         Name: {instance.ContectUs_name}
    #         Email: {instance.ContectUs_email}
    #         Mobile: {instance.ContectUs_cono}
    #         Travel Date: {instance.ContectUs_Travel_Date}
    #         Message: {instance.ContectUs_message}
    #         """
    #         recipient_list = ["booking@maharajacabs.in"]  # where mail should go

    #         try:
    #             send_mail(
    #                 subject,
    #                 message,
    #                 settings.DEFAULT_FROM_EMAIL,
    #                 recipient_list,
    #                 fail_silently=False,
    #             )
    #         except Exception as e:
    #             return Response({"message": "Record created, but email sending failed", "error": str(e)}, status=status.HTTP_201_CREATED)

    #         return Response({"message": "Record created successfully & email sent", "data": serializer.data}, status=status.HTTP_201_CREATED)

    #     return Response({"message": "Failed to create record", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        serializer = ContectUsSubmitSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            subject = "New Contact Us Submission"
            message = f"""
            You have received a new contact form submission:

            Name: {instance.ContectUs_name}
            Email: {instance.ContectUs_email}
            Mobile: {instance.ContectUs_cono}
            Travel Date: {instance.ContectUs_Travel_Date}
            Message: {instance.ContectUs_message}
            """

            try:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=["sssworldturism@gmail.com","amanmangal979951@gmail.com"],  
                    bcc=["dadhich108@gmail.com", "swamitanuj60@gmail.com"], 
                )
                email.send(fail_silently=False)
            except Exception as e:
                return Response({"message": "Record created, but email sending failed", "error": str(e)}, status=status.HTTP_201_CREATED)

            return Response({"message": "Record created successfully & email sent", "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"message": "Failed to create record", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = get_object_or_404(ContectUsSubmit, pk=pk, record_status="Active")
        serializer = ContectUsSubmitSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Record updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Failed to update record", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(ContectUsSubmit, pk=pk, record_status="Active")
        obj.record_status = "Deleted"
        obj.save()
        return Response({"message": "Record marked as Deleted"}, status=status.HTTP_200_OK)


class BannerView(APIView):
    def get(self, request):
        page = request.query_params.get('page')

        if page:
            banners = banner.objects.filter(page__iexact=page)
        else:
            banners = banner.objects.all()

        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)