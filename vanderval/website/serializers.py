from rest_framework import serializers
from .models import Site, UserRecords

class SiteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['name', 'domain', 'url', 'record_capicity']  # Include specific fields from the Site model
        #fileds = '__all__'  # Include all fields from the Site model
    # def validate(self, data):
    #     # Custom validation logic
    #     if data['record_capicity'] not in [1, 2, 3]:
    #         raise serializers.ValidationError("Invalid record capacity choice.")
    #     return data

class UserRecordsSerializers(serializers.ModelSerializer):
    site = SiteSerializers()
    class Meta:
        model = UserRecords
        fields = '__all__'

