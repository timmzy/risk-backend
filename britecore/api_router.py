from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from insurance.api.views import RiskViewSet, RiskAndFieldsViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("risks", RiskViewSet)
router.register("risks-fields", RiskAndFieldsViewSet)


app_name = "api"
urlpatterns = router.urls
