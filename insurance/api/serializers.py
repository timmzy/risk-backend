from rest_framework import serializers
from insurance.models import Risk, RiskField


class RiskFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskField
        fields = ['id', 'name', 'field_type', 'kwargs']


class RiskOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ['id', 'name', 'description']


class RiskAndFieldsSerializer(serializers.ModelSerializer):
    fields = RiskFieldSerializer(many=True)

    class Meta:
        model = Risk
        fields = ['id', 'name', 'description', 'fields']
