from rest_framework import serializers
from ..models import Language, Appointment,Customer

class CreateAppointmentSerializer(serializers.ModelSerializer):
    language = serializers.CharField(write_only=True, required=True)
    planned_start_time = serializers.DateTimeField(required=True)
    planned_duration = serializers.TimeField(required=True)
    location = serializers.CharField(required=True)
    company = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.CharField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
 
    class Meta:
        model = Appointment
        fields = [
            "planned_start_time",
            "planned_duration",
            "location",
            "company",
            "gender",
            "language",
            "notes",
            "customer"
        ]
        extra_kwargs = {
            "notes": {"required": False},
            "company": {"required": False}
        }

    def create(self, validated_data):
        language = validated_data.pop("language")
        gender = validated_data.pop("gender")
        language_Object, created = Language.objects.get_or_create(
            language_name=language
        )
        appointment = Appointment.objects.create(
            **validated_data,
            language=language_Object,
            gender_preference=gender
        )
        return appointment