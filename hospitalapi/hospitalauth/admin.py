from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from hospitalauth.models import HospitalUser, Patient, Doctor, Appointment, MedicalRecord, Prescription


admin.site.register(HospitalUser)



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('gender', 'date_of_birth')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'first_name', 'last_name', 'specialization', 'years_of_experience', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'specialization')
    list_filter = ('specialization', 'years_of_experience')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'reason_for_visit', 'status')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'reason_for_visit')
    list_filter = ('appointment_date', 'appointment_time', 'status')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'patient', 'doctor', 'diagnosis', 'treatment', 'date_of_record')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'diagnosis', 'treatment')
    list_filter = ('date_of_record',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_id', 'patient', 'doctor', 'medication_name', 'dosage', 'duration', 'date_of_prescription')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'medication_name')
    list_filter = ('date_of_prescription',)


