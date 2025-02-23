from django.urls import path
from rest_framework.routers import DefaultRouter
from testing.views import TestingProblemViewSet, TestingSubmitViewSet

router = DefaultRouter()
router.register(r'testing-problem', TestingProblemViewSet)
router.register(r'testing-submit', TestingSubmitViewSet)

urlpatterns = router.urls