from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time
from django.core.files.uploadedfile import SimpleUploadedFile
from bookingandbilling.models import (Admin,
                                      Interpreter,
                                      Customer, 
                                      Tag, Language,
                                      Appointment,
                                      Translation,
                                      Gender)

'''
Set Up Base Test Case that is Run Before Every Test (if inherited)

This in itself when ran tests generic admin, interpreter, customer, tag, and language creation
'''
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

        # Create tags
        self.on_holiday = Tag.objects.create(
            name="On Holiday",
            colour="#ffff00"
        )
        self.multilingual = Tag.objects.create(
            name="Multilingual",
            colour="#0082EF"
        )

        # Create languages
        self.english = Language.objects.create(language_name="English")
        self.spanish = Language.objects.create(language_name="Spanish")
        self.french = Language.objects.create(language_name="French")
        self.german = Language.objects.create(language_name="German")

        # Create basic interpreters
        self.interpreter = Interpreter.objects.create(
            first_name="Freddy",
            last_name="Johnson",
            email="multilingualinterpreter@gmail.com",
            address="123 Real Street",
            postcode="ABCD EFG",
            gender=Gender.PREFER_NOT_TO_SAY,
            password="password",
        )
        self.interpreter.languages.add(
            self.english,
            self.spanish,
            self.french
        )
        self.interpreter.tag.add(self.multilingual)

        # Create basic customers
        self.customer_approved = Customer.objects.create(
            first_name="Bartholomew",
            last_name="Richard",
            organisation="The Institute",
            email="barthrich4000@plusnet.com",
            address="123 Real Street",
            postcode="ABCD EFG",
            password="password",
            approved=True,
            approver=self.admin1
        )
        self.customer_not_approved = Customer.objects.create(
            first_name="Yogi",
            last_name="Bear",
            organisation="The Hut",
            email="picnicbaskets@jellystone.com"
        )


'''
Test cases for admin account creation

test_basic_admin: tests the creation of an admin with the three required fields
test_full_admin: tests the creation of an admin with all fields
test_required_fields: tests that the required fields are required
test_creation_timestamp: tests that the created_at field is
auto-populated with the current timestamp
test_unique_email: tests that the email of an admin must be unique
test_email_format_validation: tests that the email of an admin
must becorrectly formatted
'''
class AdminTestCase(BaseTestCase):
    def test_basic_admin(self):
        self.assertEqual(self.admin1.first_name, "John")
        self.assertEqual(self.admin1.last_name, "Brown")
        self.assertEqual(self.admin1.email, "johnbrown@gmail.com")

    def test_full_admin(self):
        full_admin = Admin.objects.create(
            first_name="Steven",
            last_name="Gerrard",
            email="steven10gerrard@yahoo.co.uk",
            phone_number="08264829364",
            alt_phone_number="03628927465",
            notes="This is an example note, hopefully we get no errors!"
        )
        
        self.assertEqual(full_admin.first_name, "Steven")
        self.assertEqual(full_admin.last_name, "Gerrard")
        self.assertEqual(full_admin.email, "steven10gerrard@yahoo.co.uk")
        self.assertEqual(full_admin.phone_number, "08264829364")
        self.assertEqual(full_admin.alt_phone_number, "03628927465")
        self.assertEqual(
            full_admin.notes,
            "This is an example note, hopefully we get no errors!"
        )

    def test_required_fields(self):
        '''
        Although first_name, last_name, and email are
        required fields, this only is enforced for forms
        Therefore, we expect the objects to create, which
        we then check afterwards with a validation check
        
        We delete these invalid objects once done

        Additionally, due to validating using inbuilt
        Django validation, we must supply passwords
        '''

        all_included = Admin.objects.create(
            first_name="Liam",
            last_name="Murphy",
            email="notmyrealemail@gmail.com",
            password="password"
        )
        try:
            all_included.full_clean()
        except ValidationError:
            self.fail("Admin with all three required fields was flagged as invalid")

        missing_email = Admin.objects.create(
            first_name="Ben",
            last_name="Everest",
            password="password"
        )
        with self.assertRaises(ValidationError):
            missing_email.full_clean()
        missing_email.delete()

        missing_first_name = Admin.objects.create(
            email="fakeemail@btinternet.com",
            last_name="George",
            password="password"
        )
        with self.assertRaises(ValidationError):
            missing_first_name.full_clean()
        missing_first_name.delete()

        missing_last_name = Admin.objects.create(
            first_name="Lillia",
            email="lillia@gmail.com",
            password="password"
        )
        with self.assertRaises(ValidationError):
            missing_last_name.full_clean()
        missing_last_name.delete()
        
        missing_all = Admin.objects.create(password="password")
        with self.assertRaises(ValidationError):
            missing_all.full_clean()
        missing_all.delete()

    def test_creation_timestamp(self):
        '''
        Checks that the object was created within 10s of the recorded creation_time
        '''
        new_admin = Admin.objects.create()
        time_difference = timezone.now() - new_admin.date_joined
        self.assertLessEqual(abs(time_difference.total_seconds()), 10)

    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            Admin.objects.create(email="johnbrown@gmail.com") # email is used in setup

    def test_email_format_validation(self):
        '''
        Email field has a validator on it that should return a
        ValidationError if an invalid email is provided
        '''

        incorrect_emails = [
            "plainaddress", # no @, domain or tld
            "missingatsign.com", # no @ or domain
            "missingdomain@.com", # no domain
            "@missingusername.com", # no username
            "missing@domain@domain.com", # double @
            "username@domain..com", # double period
            "user@domain,com", # comma instead of period
            "user@domain#example.com", # illegal domain character
            "user@domaincom", # no tld
            "user@domain.com." # trailing period
        ]

        dummy_admin = Admin.objects.create(
            first_name="Dummy",
            last_name="Admin",
            password="password"
        )

        for incorrect_email in incorrect_emails:
            dummy_admin.email = incorrect_email
            dummy_admin.save()

            with self.assertRaises(ValidationError):
                dummy_admin.full_clean()

        dummy_admin.email = "validemail@gmail.com"
        dummy_admin.save()
        try:
            dummy_admin.full_clean()
        except ValidationError:
            self.fail("Admin with correct email flagged as invalid")


'''
Test cases for interpreter account creation

NOTE: User parent model features already tested
in the admin tests are not tested again
ie email is unique, email validation, date_joined timestamp

NOTE: Language and Tags are not tested here as they are
tested in their respective test cases

test_basic_interpreter: tests the creation of an interpreter with the five required fields
test_full_interpreter: tests the creation of an interpreter with all fields
'''
class InterpreterTestCase(BaseTestCase):

    def test_basic_interpreter(self):
        self.assertEqual(self.interpreter.first_name,"Freddy")
        self.assertEqual(self.interpreter.last_name, "Johnson")
        self.assertEqual(self.interpreter.email, "multilingualinterpreter@gmail.com")
        self.assertEqual(self.interpreter.address, "123 Real Street")
        self.assertEqual(self.interpreter.postcode, "ABCD EFG")
        self.assertEqual(self.interpreter.gender, Gender.PREFER_NOT_TO_SAY)
        
        try:
            self.interpreter.full_clean()
        except ValidationError:
            self.fail("Interpreter with all five required fields was flagged as invalid")

    def test_full_interpreter(self):
        full_interpreter = Interpreter.objects.create(
            first_name="Clara",
            last_name="Murphy",
            email="fakeraddress@gmail.com",
            address="123 Fake Street",
            postcode="AB12 3CD",
            gender=Gender.FEMALE,
            phone_number="01234567890",
            alt_phone_number="09876543210",
            notes="This is some fake notes\nthere shouldn't be any problems with this"
        )
        
        self.assertEqual(full_interpreter.first_name , "Clara")
        self.assertEqual(full_interpreter.last_name , "Murphy")
        self.assertEqual(full_interpreter.email , "fakeraddress@gmail.com")
        self.assertEqual(full_interpreter.address, "123 Fake Street")
        self.assertEqual(full_interpreter.postcode, "AB12 3CD")
        self.assertEqual(full_interpreter.gender, Gender.FEMALE)
        self.assertEqual(full_interpreter.phone_number, "01234567890")
        self.assertEqual(full_interpreter.alt_phone_number, "09876543210")
        self.assertEqual(
            full_interpreter.notes,
            "This is some fake notes\nthere shouldn't be any problems with this"
        )


'''
Test cases for customer account creation

NOTE: User parent model features already tested in the admin
tests are not tested again
ie email is unique, email validation, date_joined timestamp

test_basic_customer: tests the creation of an customer with the five required fields
test_full_customer: tests the creation of an customer with all fields

NOTE: While ideally we would not need to test the approvement
logic again (like we do in interpreter)
the logic cannot be guaranteed to be identical as while the
code should be near identical, they cannot
share the same fields (from an abstract class) as the reference_name
in Admin needs to be different for interpreters and customers

test_default_approved: tests the default state of the approved field
test_approving: tests updating the approval status of an customer
test_approver_deletion: tests deleting the approver of an customer
'''
class CustomerTestCase(BaseTestCase):

    def test_basic_customer(self):
        self.assertEqual(self.customer_approved.first_name, "Bartholomew")
        self.assertEqual(self.customer_approved.last_name, "Richard")
        self.assertEqual(self.customer_approved.email, "barthrich4000@plusnet.com")
        self.assertEqual(self.customer_approved.address, "123 Real Street")
        self.assertEqual(self.customer_approved.postcode, "ABCD EFG")

        try:
            self.customer_approved.full_clean()
        except ValidationError:
            self.fail("Customer with all five required fields was flagged as invalid")

    def test_full_customer(self):
        full_customer = Customer.objects.create(
            first_name="Clara",
            last_name="Murphy",
            organisation="Fake Company",
            email="fakeraddress@gmail.com",
            approved=True,
            approver=self.admin1,
            address="123 Fake Street",
            postcode="AB12 3CD",
            phone_number="01234567890",
            alt_phone_number="09876543210",
            notes="This is some fake notes\nthere shouldn't be any problems with this"
        )
        
        self.assertEqual(full_customer.first_name , "Clara")
        self.assertEqual(full_customer.last_name , "Murphy")
        self.assertEqual(full_customer.organisation, "Fake Company")
        self.assertEqual(full_customer.email , "fakeraddress@gmail.com")
        self.assertTrue(full_customer.approved)
        self.assertEqual(full_customer.approver, self.admin1)
        self.assertEqual(full_customer.address, "123 Fake Street")
        self.assertEqual(full_customer.postcode, "AB12 3CD")
        self.assertEqual(full_customer.phone_number, "01234567890")
        self.assertEqual(full_customer.alt_phone_number, "09876543210")
        self.assertEqual(
            full_customer.notes,
            "This is some fake notes\nthere shouldn't be any problems with this"
        )

    def test_default_approved(self):
        # customer did not have approval set in setup
        self.assertFalse(self.customer_not_approved.approved)

    def test_approving(self):
        self.customer_not_approved.approved = True
        self.customer_not_approved.approver = self.admin2
        self.customer_not_approved.save()

        self.assertTrue(self.customer_not_approved.approved)
        self.assertEqual(self.customer_not_approved.approver, self.admin2)
        self.assertIn(
            self.customer_not_approved,
            self.admin2.approved_customers.all()
        )

    def test_approver_deletion(self):
        self.admin1.delete()
        # need to refetch the interpreter as the values are cached
        uncached_customer = Customer.objects.get(id=self.customer_approved.id)
        self.assertIsNone(uncached_customer.approver)


'''
Test cases for tag creation

test_basic_tag_creation: tests creation of a tag
test_default_colour: tests that with no provided
colour a tag will have the colour #FFFFFF
test_colour_regex: tests that the colour field only accepts valid hexcodes
test_association_with_interpreter: tests the many-to-many
relationship between tags and interpreters
'''
class TagTestCase(BaseTestCase):
    
    def test_basic_tag_creation(self):
        self.assertEqual(self.on_holiday.name, "On Holiday")
        self.assertEqual(self.on_holiday.colour, "#ffff00")

    def test_required_fields(self):
        tag = Tag.objects.create()

        with self.assertRaises(ValidationError):
            tag.full_clean()
        
        tag.name = "Name"
        tag.save()

        try:
            tag.full_clean()
        except ValidationError:
            self.fail("Tag with name was flagged as invalid")

    def test_default_colour(self):
        default_colour = Tag.objects.create()
        self.assertEqual(default_colour.colour, "#FFFFFF")

    def test_colour_regex(self):
        '''
        Colour field has a validator on it that should return a
        ValidationError if an invalid hexcode is provided
        '''

        incorrect_colours = [
            "123456", # no hastag
            "#12345", # missing character
            "1234#21", # does not start with hashtag
            "#G12345" # G is not a valid character
        ]

        dummy_tag = Tag.objects.create(name="Dummy")

        for incorrect_colour in incorrect_colours:
            dummy_tag.colour = incorrect_colour
            dummy_tag.save()

            with self.assertRaises(ValidationError):
                dummy_tag.full_clean()

        dummy_tag.colour = "#1234AB"
        dummy_tag.save()
        try:
            dummy_tag.full_clean()
        except ValidationError:
            self.fail("Tag with correct colour flagged as invalid")

    def test_association_with_interpreter(self):
        self.assertEqual(self.multilingual.interpreters.count(), 1)
        self.assertIn(self.interpreter, self.multilingual.interpreters.all())
        self.assertIn(self.multilingual, self.interpreter.tag.all())


'''
Test cases for language creation

test_basic_language_creation: tests creation of a language
test_association_with_interpreter: tests the many-to-many
relationship between languages and interpreters
'''
class LanguageTestCase(BaseTestCase):
    
    def test_basic_language_creation(self):
        self.assertEqual(self.english.language_name, "English")

    def test_required_fields(self):
        language = Language.objects.create()

        with self.assertRaises(ValidationError):
            language.full_clean()
        
        language.language_name = "Name"
        language.save()

        try:
            language.full_clean()
        except ValidationError:
            self.fail("Language with name was flagged as invalid")

    def test_association_with_interpreter(self):
        self.assertEqual(self.english.interpreters.count(), 1)
        self.assertIn(self.interpreter, self.english.interpreters.all())
        self.assertIn(self.english, self.interpreter.languages.all())


'''
Test cases for appointment creation

insert tests and descriptions here
'''
class AppointmentTestCase(BaseTestCase):

    def test_required_fields(self):
        '''
        COULD ADD A TEST TO ENSURE ALL OF THESE ARE REQUIRED FIELDS,
        CURRENTLY JUST TESTS THAT THE REQUIRED FIELDS ARE A SUBSET OF THESE
        '''
        appointment = Appointment.objects.create(
            customer=self.customer_approved,
            planned_start_time=timezone.make_aware(datetime(2024,12,1,9,0)),
            planned_duration=time(1,30),
            location="Glasgow",
            language=self.spanish
        )

        try:
            appointment.full_clean()
        except ValidationError:
            self.fail("Appointment with all five required fields was flagged as invalid")

    def test_full_appointment(self):
        appointment = Appointment.objects.create(
            customer=self.customer_approved,
            planned_start_time=timezone.make_aware(datetime(2024,12,1,9,0)),
            planned_duration=time(1,30),
            location="Glasgow",
            language=self.spanish,
            interpreter=self.interpreter,
            admin=self.admin1,
            actual_start_time=timezone.make_aware(datetime(2024,12,1,9,10)),
            actual_duration=time(1,15),
            status="Cancelled",
            gender_preference=Gender.MALE,
            notes="This is a test, let's hope\nthat the notes are stored correctly!",
            active=False
        )

        self.assertEqual(appointment.customer, self.customer_approved)
        self.assertEqual(
            appointment.planned_start_time,
            timezone.make_aware(datetime(2024,12,1,9,0))
        )
        self.assertEqual(appointment.planned_duration, time(1,30))
        self.assertEqual(appointment.location, "Glasgow")
        self.assertEqual(appointment.language, self.spanish)
        self.assertEqual(appointment.interpreter, self.interpreter)
        self.assertEqual(appointment.admin, self.admin1)
        self.assertEqual(
            appointment.actual_start_time,
            timezone.make_aware(datetime(2024,12,1,9,10))
        )
        self.assertEqual(appointment.actual_duration, time(1,15))
        self.assertEqual(appointment.status, "Cancelled")
        self.assertEqual(appointment.gender_preference, Gender.MALE)
        self.assertEqual(
            appointment.notes,
            "This is a test, let's hope\nthat the notes are stored correctly!"
        )
        self.assertFalse(appointment.active)

    def test_admin_assigning_appointment(self):
        '''
        Appointment is created with a planned_start_time
        and planned_duration to prevent an Integrity error
        '''
        appointment = Appointment.objects.create(
            planned_start_time=timezone.make_aware(datetime(2024,12,1,9,0)),
            planned_duration=time(1,30)
        )
        appointment.interpreter = self.interpreter
        appointment.admin = self.admin1
        appointment.save()
        
        self.assertEqual(appointment.interpreter, self.interpreter)
        self.assertTrue(appointment in self.interpreter.appointments.all())

        self.assertEqual(appointment.admin, self.admin1)
        self.assertTrue(appointment in self.admin1.appointments.all())

    def test_customer_relation(self):
        '''
        Appointment is created with a planned_start_time
        and planned_duration to prevent an Integrity error
        '''
        appointment = Appointment.objects.create(
            customer=self.customer_approved,
            planned_start_time=timezone.make_aware(datetime(2024,12,1,9,0)),
            planned_duration=time(1,30)
        )

        self.assertEqual(appointment.customer, self.customer_approved)
        self.assertTrue(appointment in self.customer_approved.appointments.all())

    def test_defaults(self):
        '''
        Appointment is created with a planned_start_time
        and planned_duration to prevent an Integrity error
        '''
        appointment = Appointment.objects.create(
            planned_start_time=timezone.make_aware(datetime(2024,12,1,9,0)),
            planned_duration=time(1,30)
        )
        self.assertEqual(appointment.status, "Upcoming")
        self.assertTrue(appointment.active)
        self.assertEqual(appointment.gender_preference, Gender.PREFER_NOT_TO_SAY)


'''
Test cases for translation creation

insert tests and descriptions here
'''
class TranslationTestCase(BaseTestCase):

    def test_required_fields(self):
        '''
        COULD ADD A TEST TO ENSURE ALL OF THESE ARE REQUIRED FIELDS,
        CURRENTLY JUST TESTS THAT THE REQUIRED FIELDS ARE A SUBSET OF THESE
        '''
        translation = Translation.objects.create(
            customer=self.customer_approved,
            word_count=100,
            language=self.spanish,
            document=SimpleUploadedFile("test_document.txt", b"Document content to be translated")
        )

        try:
            translation.full_clean()
        except ValidationError:
            self.fail("Translation with all four required fields was flagged as invalid")        

    def test_invalid_word_count(self):
        incorrect_word_counts = [
            -1,
            -999,
            0
        ]

        for incorrect_word_count in incorrect_word_counts:
            with self.assertRaises(ValidationError):
                translation = Translation(
                    customer=self.customer_approved,
                    language=self.spanish,
                    document=SimpleUploadedFile(
                        "test_document.txt",
                        b"Document content to be translated"
                    ),
                    word_count=incorrect_word_count
                )
                translation.full_clean()

    def test_full_translation(self):
        translation = Translation.objects.create(
            customer=self.customer_approved,
            language=self.spanish,
            document=SimpleUploadedFile(
                "test_document.txt",
                b"Document content to be translated"
            ),
            word_count=5,
            interpreter=self.interpreter,
            admin=self.admin1,
            notes="This is a test, let's hope\nthat the notes are stored correctly!",
            active=False
        )

        self.assertEqual(translation.customer, self.customer_approved)
        self.assertEqual(translation.language, self.spanish)
        self.assertEqual(translation.interpreter, self.interpreter)
        self.assertEqual(translation.admin, self.admin1)
        self.assertEqual(translation.word_count, 5)
        self.assertEqual(
            translation.notes,
            "This is a test, let's hope\nthat the notes are stored correctly!"
        )
        self.assertFalse(translation.active)

        with translation.document.open("rb") as f:
            self.assertEqual(f.read(), b"Document content to be translated")

    def test_admin_assigning_appointment(self):
        translation = Translation.objects.create(word_count=1)
        translation.interpreter = self.interpreter
        translation.admin = self.admin1
        translation.save()
        
        self.assertEqual(translation.interpreter, self.interpreter)
        self.assertTrue(translation in self.interpreter.translations.all())

        self.assertEqual(translation.admin, self.admin1)
        self.assertTrue(translation in self.admin1.translations.all())

    def test_customer_relation(self):
        translation = Translation.objects.create(customer=self.customer_approved, word_count=1)

        self.assertEqual(translation.customer, self.customer_approved)
        self.assertTrue(translation in self.customer_approved.translations.all())

    def test_defaults(self):
        translation = Translation.objects.create(word_count=1)
        self.assertTrue(translation.active)
