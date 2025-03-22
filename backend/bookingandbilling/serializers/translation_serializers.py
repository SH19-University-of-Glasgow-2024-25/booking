from rest_framework import serializers
from ..models import Language, Translation, Customer

class CreateTranslationSerializer(serializers.ModelSerializer):
    document = serializers.FileField(required=True)
    language = serializers.CharField(write_only=True, required=True)
    word_count = serializers.CharField(required=True)
    company = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)

    class Meta:
        model = Translation
        fields = [
            "document",
            "language",
            "word_count",
            "company",
            "notes",
            "customer"
        ]
        extra_kwargs = {
            "company": {"required": False},
            "notes": {"required": False},
        }

    def create(self, validated_data):
        language = validated_data.pop("language")
        language_Object, created = Language.objects.get_or_create(
            language_name=language
        )
        translation = Translation.objects.create(
            **validated_data,
            language=language_Object
        )
        
        return translation
    
        
