from rest_framework import serializers
from ..models import Interpreter, Appointment, Tag, Language, Customer, Translation

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "colour"]

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "language_name"]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name']

class InterpreterSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    tag = TagSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    offered_translations = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True  # Prevent updates through this field
    )
    offered_appointments = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True  # Prevent updates through this field
    )

    class Meta:
        model = Interpreter
        fields = ['id', 'first_name', 'last_name', 'languages', 'email',
                  'tag', 'offered_translations', 'offered_appointments', 'gender']

    def get_gender(self, obj):
        return obj.get_gender_display()

class GetAppointmentSerializer(serializers.ModelSerializer):
    gender_preference = serializers.SerializerMethodField()
    customer = CustomerSerializer(read_only=True)
    interpreter = InterpreterSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    planned_start_time = serializers.SerializerMethodField()
    actual_start_time = serializers.SerializerMethodField()
    planned_duration = serializers.SerializerMethodField()
    actual_duration = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'interpreter', 'language', 
                  'gender_preference', 'planned_start_time', 
                  'actual_start_time', 'planned_duration', 'actual_duration',
                  'location', 'company', 'invoice_generated']

    def get_gender_preference(self, obj):
        return obj.get_gender_preference_display()

    def format_datetime(self, dt):
        return dt.strftime('%B %d, %Y %I:%M %p') if dt else None

    def get_planned_start_time(self, obj):
        return self.format_datetime(obj.planned_start_time)

    def get_actual_start_time(self, obj):
        return self.format_datetime(obj.actual_start_time)
    
    def format_duration(self, time):
        if time:
            hours, minutes = time.hour, time.minute
            if hours and minutes:
                return f"{hours} hours {minutes} minutes"
            elif minutes:
                return f"{minutes} minutes"
            elif hours:
                return f"{hours} hours"
        return None

    def get_planned_duration(self, obj):
        return self.format_duration(obj.planned_duration)

    def get_actual_duration(self, obj):
        return self.format_duration(obj.actual_duration)  
    
class GetTranslationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    interpreter = InterpreterSerializer(read_only=True)

    class Meta:
        model = Translation
        fields = ['id', 'customer', 'language', 'interpreter',
                  'word_count', 'actual_word_count', 'document', 'company', 'invoice_generated']
