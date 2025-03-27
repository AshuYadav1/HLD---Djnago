# myapp/serializers.py
from rest_framework import serializers

class CampaignSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2)