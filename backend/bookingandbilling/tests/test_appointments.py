from django.test import TestCase

from bookingandbilling.serializers.appointment_serializers import (
    CreateAppointmentSerializer
)
from bookingandbilling.models import (
    Admin,
    Customer,
    Language,
    Appointment
)

class BaseTestCase(TestCase):
    
    def setUp(self):
        # Create basic admins
        self.admin1 = Admin.objects.create(
            first_name="John",
            last_name="Brown",
            email="johnbrown@gmail.com"
        )
        self.admin2 = Admin.objects.create(
            first_name="Amanda",
            last_name="Prentice",
            email="amandaprentice@gmail.com"
        )

        # Create languages
        self.english = Language.objects.create(language_name="English")
        self.spanish = Language.objects.create(language_name="Spanish")
        self.french = Language.objects.create(language_name="French")
        self.german = Language.objects.create(language_name="German")

        # Create basic customers
        self.customer1 = Customer.objects.create(
            first_name="Bartholomew",
            last_name="Richard",
            email="barthrich4000@plusnet.com",
            address="123 Real Street",
            postcode="ABCD EFG",
            password="password",
            approved=True,
            approver=self.admin1
        )
        self.data = {
            "customer": self.customer1,
            "language":"french",
            "location":"here",
            "planned_start_time":"2025-01-24T20:00",
            "planned_duration":"01:00",
            "gender":"X",
            "notes":"notey note note"
        }
        
        
class AppointmentSerializerTestCase(BaseTestCase):
    """
    
    Test appointment creation serializer

    test_valid_data: test serializer with valid data

    
    """

    def test_valid_data(self):
        serializer = CreateAppointmentSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        appointment = serializer.save()
        self.assertEqual(appointment.__class__, Appointment)
        
    def test_valid_data_without_optional_data(self):
        self.data.pop("notes")
        serializer = CreateAppointmentSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        appointment = serializer.save()
        self.assertEqual(appointment.__class__, Appointment)
        
    def test_required_fields(self):
        required_fields = [
            "customer",
            "language",
            "location",
            "planned_start_time",
            "planned_duration",
            "gender"
        ]

        for required_field in required_fields:
            temp = self.data.pop(required_field)
            serializer = CreateAppointmentSerializer(data=self.data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(required_field, serializer.errors)
            self.data[required_field] = temp

    def test_invalid_data(self):
        self.data["customer"] = "not a customer"
        serializer = CreateAppointmentSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("customer", serializer.errors)
        self.data["customer"] = self.customer1