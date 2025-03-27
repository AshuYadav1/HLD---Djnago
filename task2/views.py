# myapp/views.py
from rest_framework import views
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response

from .serializers import CampaignSerializer
from .task import process_campaign
import logging

logger = logging.getLogger(__name__)

class CreateCampaignView(views.APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            agency = request.user.agency
            logger.info(f"Campaign created by agency {agency.id}: {serializer.validated_data}")
            process_campaign.delay(serializer.validated_data)  # Enqueue task
            return Response({"status": "success", "data": serializer.validated_data}, status=201)
        logger.error(f"Invalid campaign data: {serializer.errors}")
        return Response(serializer.errors, status=400)