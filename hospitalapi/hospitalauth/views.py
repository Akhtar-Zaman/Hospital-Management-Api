from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from hospitalauth.serializers import UserRegistrationSerializer, UserLoginSerializer, HospitalUserListSerializer, PatientSerializer, DoctorSerializer, AppointmentSerializer, MedicalRecordSerializer, PrescriptionSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .models import HospitalUser, Patient, Doctor, Appointment, MedicalRecord, Prescription
import json
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        response = requests.post(f'{settings.BACKEND_URL}/hospital/api/user/login/', data={
            'email': email,
            'password': password
        })
        if response.status_code == 200:
            data = response.json()
            

            token = response.json().get('token')
            request.session['token'] = token
            return redirect('hospitalauth:profile')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'hospitalauth/login.html', {'error': 'Invalid username or password'})

    return render(request, 'hospitalauth/login.html')

def profile_view(request):
    token = request.session.get('token')
    if not token:
        return redirect('hospitalauth:login')
    headers = {
        'Authorization': f'Bearer {token['access']}'
    }
    response = requests.get(f'{settings.BACKEND_URL}/hospital/api/user/some-protected-endpoint/', headers=headers)
    if response.status_code == 200:
        user = request.user
        data = response.json()
        print("############# udd", data)
        return render(request, 'hospitalauth/profile.html', {'data': data,
                                                            })
    else:
        return redirect('hospitalauth:login')
    

def home_view(request):
        return render(request, 'hospitalauth/index.html')
    
@csrf_exempt
def edit_appointment(request):
    print("############## 0000 ##########", request)
    if request.method == 'POST':
        appointment_id = request.POST.get('id')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.patient.first_name = request.POST.get('patient_name')
        appointment.doctor.first_name = request.POST.get('doctor_name')
        appointment.appointment_date = request.POST.get('appointment_date')
        appointment.appointment_time = request.POST.get('appointment_time')
        appointment.reason_for_visit = request.POST.get('reason_for_visit')
        appointment.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        date_of_birth = request.POST['date_of_birth']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'hospitalauth/login.html')

        if HospitalUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, 'hospitalauth/login.html')

        user = HospitalUser.objects.create_user(
            name=name,
            email=email,
            address=address,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            is_doctor=True,
        )

        user.set_password(password)
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('hospitalauth:login')
    
    return render(request, 'hospitalauth/login.html')


class SomeProtectedEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     user = request.user
    #     # appointments_list = {}
    #     # if user.is_doctor:
    #     #     appointments_query = Appointment.objects.filter(doctor__email=user.email)
    #     #     for appointment in appointments_query:
    #     #         data = {
    #     #             'patient': appointment.patient.first_name,
    #     #             'doctor': appointment.doctor.first_name,
    #     #             'appointment_date': appointment.appointment_date,
    #     #             'appointment_time': appointment.appointment_time,
    #     #             'reason_for_visit': appointment.reason_for_visit,
    #     #         }
    #     #         appointments_list.update(data)
    #     #         print("############## app ############", appointments_list)
    #     # elif user.is_patient:
    #     appointments = Appointment.objects.filter(doctor__email=user.email)
    #     user_info = {
    #         'name': user.name,
    #         'email': user.email,
    #         'role':  'doctor' if user.is_doctor  else 'patient'
    #     }
    #     return Response({'message': 'You have access to this protected endpoint', 'user_info': user_info, 'appointments': appointments.json()})

    def get(self, request):
        user = request.user
        
        # Fetch appointments based on the user's role
        if user.is_doctor:
            appointments = Appointment.objects.filter(doctor__email=user.email)
        elif user.is_patient:
            appointments = Appointment.objects.filter(patient=user)
        else:
            appointments = []

        # Serialize the appointments data
        serializer = AppointmentSerializer(appointments, many=True)

        user_info = {
            'name': user.name,
            'email': user.email,
            'role': 'doctor' if user.is_doctor else 'patient'
        }

        return Response({
            'message': 'You have access to this protected endpoint',
            'user_info': user_info,
            'appointments': serializer.data
        })



class HospitalUserRegitrationView(APIView):

# {
#     "name": "Akhtaruzzaman Khan",
#     "email": "akhtar@gmail.com",
#     "address": "39939 Stevenson Common",
#     "date_of_birth": "18 September 1997",
#     "phone_number": "555555555",
#     "password": "123",
#     "password2": "123"
# }

    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registered Succesfully'})

class UserListView(generics.ListAPIView):
    queryset = HospitalUser.objects.all()
    serializer_class = HospitalUserListSerializer
    
class HospitalUserLoginView(APIView):
    
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Successfull', 'details': request.data}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'User Is Not Valid'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientViewSet(viewsets.ModelViewSet):
#     {
#     "first_name": "John",
#     "last_name": "Doe",
#     "date_of_birth": "1980-01-01",
#     "gender": "Male",
#     "address": "123 Main St, Springfield",
#     "phone_number": "123-456-7890",
#     "email": "john.doe@example.com",
#     "medical_history": "No significant medical history",
#     "current_medications": "None",
#     "allergies": "None",
#     "emergency_contact": "Jane Doe, 123-456-7891"
# }
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DoctorViewSet(viewsets.ModelViewSet):
#     {
#     "first_name": "Alice",
#     "last_name": "Smith",
#     "specialization": "Cardiology",
#     "years_of_experience": 10,
#     "phone_number": "234-567-8901",
#     "email": "alice.smith@example.com",
#     "working_hours": "9am - 5pm",
#     "department": "Cardiology",
#     "room_number": "101"
# }
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
#     {
#     "patient": 1,
#     "doctor": 1,
#     "appointment_date": "2024-07-20",
#     "appointment_time": "10:00:00",
#     "reason_for_visit": "Routine check-up",
#     "status": "Scheduled"
# }
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class MedicalRecordViewSet(viewsets.ModelViewSet):
#     {
#     "patient": 2,
#     "doctor": 2,
#     "diagnosis": "Chronic Migraine",
#     "treatment": "Preventive medication, Pain relief",
#     "date_of_record": "2024-07-19",
#     "notes": "Patient advised to keep a headache diary and avoid known triggers."
# }
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

