from rest_framework import serializers
from insurance.models import Risk, RiskField, EnumChoice


class EnumChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumChoice
        fields = ['id', 'choice', 'value']


class RiskFieldSerializer(serializers.ModelSerializer):
    choices = EnumChoiceSerializer(many=True)

    class Meta:
        model = RiskField
        fields = ['id', 'name', 'field_type', 'kwargs', 'choices']


class RiskOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ['id', 'name', 'description']


class RiskAndFieldsSerializer(serializers.ModelSerializer):
    fields = RiskFieldSerializer(many=True)

    class Meta:
        model = Risk
        fields = ['id', 'name', 'description', 'fields']
