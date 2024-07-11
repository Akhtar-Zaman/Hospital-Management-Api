
from django.urls import path
from hospitalauth.views import HospitalUserRegitrationView, HospitalUserLoginView, UserListView


urlpatterns = [
    path('user/register/', HospitalUserRegitrationView.as_view(), name='register'),
    path('user/login/', HospitalUserLoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='userlist'),
]
