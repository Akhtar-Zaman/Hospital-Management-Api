from rest_framework import serializers
from hospitalauth.models import HospitalUser

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