from rest_framework.routers import DefaultRouter
from .views import PromptsViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'prompts', PromptsViewSet)

urlpatterns = router.urls

# urlpatterns += [
#     path('db/create/', views.create_db_view, name='create_db'), 
#     path('db/load/', views.load_db_view, name='load_db'),
# ]