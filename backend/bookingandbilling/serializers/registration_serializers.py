from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from ..models import Tag, Language, Admin, Interpreter, Customer


class RegisterAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Admin
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "phone_number",
            "alt_phone_number",
            "notes",
        ]
        extra_kwargs = {
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False},
            "notes": {"required": False},
        }

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        admin = Admin.objects.create(**validated_data)
        
        try:
            admin.set_password(validated_data["password"])
            admin.save()
            admin.full_clean()
        except Exception as e:
            admin.delete()
            raise e

        return admin
    
class RegisterInterpreterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    languages = serializers.ListField(
        child=serializers.CharField(), 
        required=False,
        write_only=True,
    )
    tag = serializers.ListField(
        child=serializers.CharField(), 
        required=False,
        write_only=True,
    )

    class Meta:
        model = Interpreter
        fields = [
            "email",
            "first_name",
            "last_name",
            "address",
            "postcode",
            "gender",
            "tag",
            "languages",
            "password",
            "confirm_password",
            "phone_number",
            "alt_phone_number",
            "notes",
        ]
        extra_kwargs = {
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False},
            "notes": {"required": False},
        }

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        language_names = validated_data.pop("languages", [])
        tag_names = validated_data.pop("tag", [])

        interpreter = Interpreter.objects.create(**validated_data)

        try:
            language_objects = []
            for name in language_names:
                language, created = Language.objects.get_or_create(
                    language_name=name
                )
                language_objects.append(language)
            interpreter.languages.set(language_objects)
            
            tag_objects = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=name
                )
                tag_objects.append(tag)
            interpreter.tag.set(tag_objects)
            
            interpreter.set_password(validated_data["password"])
            interpreter.save()
            interpreter.full_clean()
        except Exception as e:
            interpreter.delete()
            raise e

        return interpreter
    
class RegisterCustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = [
            "email",
            "first_name",
            "last_name",
            "organisation",
            "address",
            "postcode",
            "password",
            "confirm_password",
            "phone_number",
            "alt_phone_number",
            "notes",
        ]
        extra_kwargs = {
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False},
            "notes": {"required": False},
        }

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        customer = Customer.objects.create(**validated_data)
        
        try:
            customer.set_password(validated_data["password"])
            customer.save()
            customer.full_clean()
        except Exception as e:
            customer.delete()
            raise e

        return customer  