from rest_framework.routers import DefaultRouter
from .views import PromptsViewSet

router = DefaultRouter()
router.register(r'prompts', PromptsViewSet)

urlpatterns = router.urls
