from bmstu_lab.models import Services, Applications
from rest_framework import serializers


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ["name", "text", "type"]

class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = ["id", "user", "status", "created_date", "ended_date", "modified_date", "moderator", "services"]

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ["id", "name", "image", "text", "type", "price", "published"]


