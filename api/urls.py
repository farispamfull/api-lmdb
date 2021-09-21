from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from .views import (EmailConfirmationView, SignUpApiView, TitleViewSet,
                    GenreViewSet, CategoryViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('titles', TitleViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
auth_patterns = [
    path('token/',
         EmailConfirmationView.as_view(),
         name='token_obtain_pair'),
    path('signup/',
         SignUpApiView.as_view(),
         name='confirmation_code_request'),
]
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns)),
]
