from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'query', views.QueryViewSet, basename='query')
router.register(r'treatment', views.TreatmentViewSet, basename='treatment')

urlpatterns = [
    path('api/', include(router.urls)),  
    path('accounts/', include('allauth.urls')),
]