from .serializers import SiteSerializers, UserRecordsSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Site
from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import AllowAny


class SiteViewAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SiteSerializers(data = request.data)
        try:

            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                domain = serializer.validated_data.get('domain')
                url = serializer.validated_data.get('url')
                record_capicity = serializer.validated_data.get('record_capicity')
                
                description = request.data.get('description')

                SiteObject = Site.objects.create(
                    name = name,
                    domain = domain,
                    url = url,
                    record_capicity = record_capicity,
                    description = description

                )
                SiteObject.save()

                return Response({"Success": True}, status=status.HTTP_201_CREATED)

            return Response({"success" : False, "errors" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
