from rest_framework.routers import DefaultRouter
from users.views import SponsorViewSet

router = DefaultRouter()
router.register('', SponsorViewSet, basename='sponsor')
urlpatterns = router.urls
