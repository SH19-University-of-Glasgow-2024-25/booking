from rest_framework import serializers
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from ..models import Admin, Customer, Interpreter, Language, Tag
from ..serializers.registration_serializers import (RegisterAdminSerializer, 
                                                    RegisterCustomerSerializer, 
                                                    RegisterInterpreterSerializer)

# Based on https://stackoverflow.com/a/36419160 (CC BY-SA 4.0)
def validate_password(data, UserType):
    if "password" not in data:
        return
    
    # here data has all the fields which have validated values
    # so we can create a User instance out of it
    user = UserType(**data)
    
    # get the password from the data
    password = data.get('password')
    
    errors = dict() 
    try:
        # validate the password and catch the exception
        validators.validate_password(password=password, user=user)
    
    # the exception raised here is different than serializers.ValidationError
    except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)
    
    if errors:
        raise serializers.ValidationError(errors)

class AdminEditAdminSerializer(RegisterAdminSerializer):
    password = serializers.CharField(
        required=False,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Admin
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "alt_phone_number",
            "notes"
        ]
        extra_kwargs = {
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False},
            "password": {"required": False}
        }
    
    def update(self, instance, validated_data):
        if "confirm_password" in validated_data:
            validated_data.pop("confirm_password")

        try:
            for key, value in validated_data.items():
                setattr(instance, key, value)

            if "password" in validated_data:
                instance.set_password(validated_data["password"])
            instance.save()
            instance.full_clean()
        except Exception as e:
            raise e

        return instance
    
    def validate(self, data):
        validate_password(data, Admin)
        return data

class AdminEditInterpreterSerializer(RegisterInterpreterSerializer):
    password = serializers.CharField(
        required=False,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Interpreter
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
            "postcode",
            "gender",
            "tag",
            "languages",
            "phone_number",
            "alt_phone_number",
            "notes"
        ]
        extra_kwargs = {
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False},
            "notes": {"required": False},
            "password": {"required": False}
        }
    
    def update(self, instance, validated_data):
        if "confirm_password" in validated_data:
            validated_data.pop("confirm_password")

        language_names = validated_data.pop("languages", [])
        tag_names = validated_data.pop("tag", [])

        try:
            for key, value in validated_data.items():
                setattr(instance, key, value)

            language_objects = []
            for name in language_names:
                language, created = Language.objects.get_or_create(
                    language_name=name
                )
                language_objects.append(language)
            instance.languages.set(language_objects)
            
            tag_objects = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=name
                )
                tag_objects.append(tag)
            instance.tag.set(tag_objects)
            
            if "password" in validated_data:
                instance.set_password(validated_data["password"])
            instance.save()
            instance.full_clean()
        except Exception as e:
            raise e

        return instance
    
    def validate(self, data):
        validate_password(data, Interpreter)
        return data

class AdminEditCustomerSerializer(RegisterCustomerSerializer):
    password = serializers.CharField(
        required=False,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Customer
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "organisation",
            "address",
            "postcode",
            "phone_number",
            "alt_phone_number",
            "notes"
        ]
        extra_kwargs = {
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False},
            "notes": {"required": False},
            "password": {"required": False}
        }
    
    def update(self, instance, validated_data):
        if "confirm_password" in validated_data:
            validated_data.pop("confirm_password")

        try:
            for key, value in validated_data.items():
                setattr(instance, key, value)
            
            if "password" in validated_data:
                instance.set_password(validated_data["password"])
            instance.save()
            instance.full_clean()
        except Exception as e:
            raise e

        return instance
    
    def validate(self, data):
        validate_password(data, Customer)
        return data

class SelfEditAdminSerializer(RegisterAdminSerializer):
    password = serializers.CharField(
        required=False,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Admin
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "alt_phone_number",
            "notes"
        ]
        extra_kwargs = {
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False}
        }
    
    def update(self, instance, validated_data):
        if "confirm_password" in validated_data:
            validated_data.pop("confirm_password")

        try:
            for key, value in validated_data.items():
                setattr(instance, key, value)
            
            if "password" in validated_data:
                instance.set_password(validated_data["password"])
            instance.save()
            instance.full_clean()
        except Exception as e:
            raise e

        return instance
    
    def validate(self, data):
        validate_password(data, Admin)
        return data

class SelfEditInterpreterSerializer(RegisterInterpreterSerializer):
    password = serializers.CharField(
        required=False,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Interpreter
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
            "postcode",
            "gender",
            "tag",
            "languages",
            "phone_number",
            "alt_phone_number"
        ]
        extra_kwargs = {
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False},
            "notes": {"required": False},
        }
    
    def update(self, instance, validated_data):
        if "confirm_password" in validated_data:
            validated_data.pop("confirm_password")

        language_names = validated_data.pop("languages", [])
        tag_names = validated_data.pop("tag", [])

        try:
            for key, value in validated_data.items():
                setattr(instance, key, value)

            language_objects = []
            for name in language_names:
                language, created = Language.objects.get_or_create(
                    language_name=name
                )
                language_objects.append(language)
            instance.languages.set(language_objects)
            
            tag_objects = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=name
                )
                tag_objects.append(tag)
            instance.tag.set(tag_objects)
            
            if "password" in validated_data:
                instance.set_password(validated_data["password"])
            instance.save()
            instance.full_clean()
        except Exception as e:
            raise e

        return instance
    
    def validate(self, data):
        validate_password(data, Interpreter)
        return data

class SelfEditCustomerSerializer(RegisterCustomerSerializer):
    password = serializers.CharField(
        required=False,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Customer
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "organisation",
            "address",
            "postcode",
            "phone_number",
            "alt_phone_number"
        ]
        extra_kwargs = {
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False},
            "notes": {"required": False},
        }
    
    def update(self, instance, validated_data):
        if "confirm_password" in validated_data:
            validated_data.pop("confirm_password")

        try:
            for key, value in validated_data.items():
                setattr(instance, key, value)

            if "password" in validated_data:
                instance.set_password(validated_data["password"])
            instance.save()
            instance.full_clean()
        except Exception as e:
            raise e

        return instance
    
    def validate(self, data):
        validate_password(data, Customer)
        return data