from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import RetrieveAPIView, ListAPIView
from insurance.models import Risk
from insurance.api.serializers import RiskOnlySerializer, RiskAndFieldsSerializer


class RiskViewSet(RetrieveAPIView, GenericViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskOnlySerializer


class RiskAndFieldsViewSet(ListAPIView, GenericViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskAndFieldsSerializer
