from django.urls import path
from rest_framework.routers import DefaultRouter
from testing.views import TestingProblemViewSet, TestingSubmitViewSet

router = DefaultRouter()
router.register(r'testing-problems', TestingProblemViewSet)
router.register(r'testing-submits', TestingSubmitViewSet)

urlpatterns = router.urls