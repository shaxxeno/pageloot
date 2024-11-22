from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExpenseViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"expenses", ExpenseViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
