from django.urls import path, include
from .views import *

app_name = "accounts"
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
]