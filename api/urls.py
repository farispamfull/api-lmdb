from django.urls import path,include
from .views import EmailConfirmationView,SignUpApiView

auth_patterns = [
    path('token/',
         EmailConfirmationView.as_view(),
         name='token_obtain_pair'),
    path('signup/',
         SignUpApiView.as_view(),
         name='confirmation_code_request'),
]
urlpatterns = [
    # path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns)),
]