from rest_framework import serializers
from hospitalauth.models import HospitalUser, Patient, Doctor, Appointment, MedicalRecord, Prescription

class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = HospitalUser
        fields = ['name', 'email', 'address', 'date_of_birth', 'phone_number', 'password', 'password2']
        extra_kwargs ={
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validate_data):
        return HospitalUser.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length = 255)

    class Meta:
        model = HospitalUser
        fields = ['email', 'password']

class HospitalUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalUser
        fields = ['id', 'name', 'email', 'address', 'date_of_birth', 'phone_number',]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.first_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.first_name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['appointment_id', 'patient_name', 'doctor_name', 'appointment_date', 'appointment_time', 'reason_for_visit']

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
