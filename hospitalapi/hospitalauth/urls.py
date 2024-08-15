
from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 

from hospitalauth.views import ( HospitalUserRegitrationView, HospitalUserLoginView, UserListView, 
                                PatientViewSet, DoctorViewSet, AppointmentViewSet, MedicalRecordViewSet, PrescriptionViewSet, SomeProtectedEndpoint)

app_name = 'hospitalauth'
urlpatterns = [
    path('user/register/', HospitalUserRegitrationView.as_view(), name='register'),
    path('user/login/', HospitalUserLoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='userlist'),
    path('register/', views.register, name='regist'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('user/some-protected-endpoint/', SomeProtectedEndpoint.as_view(), name='some-protected-endpoint'),
    path('home/', views.home_view, name='home'),
    path('patients/', PatientViewSet.as_view({'get': 'list', 'post': 'create'}), name='patient-list'),
    path('patients/<int:pk>/', PatientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='patient-detail'),
    path('doctors/', DoctorViewSet.as_view({'get': 'list', 'post': 'create'}), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='doctor-detail'),
    path('appointments/', AppointmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='appointment-list'),
    path('appointments/<int:pk>/', AppointmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='appointment-detail'),
    path('medicalrecords/', MedicalRecordViewSet.as_view({'get': 'list', 'post': 'create'}), name='medicalrecord-list'),
    path('medicalrecords/<int:pk>/', MedicalRecordViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='medicalrecord-detail'),
    path('prescriptions/', PrescriptionViewSet.as_view({'get': 'list', 'post': 'create'}), name='prescription-list'),
    path('prescriptions/<int:pk>/', PrescriptionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='prescription-detail'),

]