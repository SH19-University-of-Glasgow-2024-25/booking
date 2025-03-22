import os
import shutil
import string
import random
import json
import django
import traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
django.setup()
from django.utils import timezone
from datetime import datetime, time
from bookingandbilling.models import (Admin,
                                      Customer,
                                      Gender,
                                      Interpreter,
                                      Language,
                                      Tag,
                                      Appointment,
                                      Translation)


def populate():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    admin_json = os.path.join(script_dir, 'populateJSONs', 'admin.json')
    customer_json = os.path.join(script_dir, 'populateJSONs', 'customer.json')
    interpreter_json = os.path.join(script_dir, 'populateJSONs', 'interpreter.json')
    language_json = os.path.join(script_dir, 'populateJSONs', 'lang.json')
    tag_json = os.path.join(script_dir, 'populateJSONs', 'tags.json')
    appointment_json = os.path.join(script_dir, 'populateJSONs', 'appointments.json')

    admin_users = import_json(admin_json)
    print("Admin Data Read")
    customer_users = import_json(customer_json)
    print("Customer Data Read")
    interpreter_users = import_json(interpreter_json)
    print("Interprter Data Read")
    languages = import_json(language_json)
    print("Language Data Read")
    tags = import_json(tag_json)
    print("Tag Data Read")
    appointments = import_json(appointment_json)
    print("Appointment Data Read")
    
    for language in languages:
        add_lang(language["lang"])  
    print("Langauge Added Successfully")
    
    for tag in tags:
        add_tag(tag["tag"],tag["color"])    
    print("Tag Added Successfully")
    
    for admin_user in admin_users:
        add_admin(
            admin_user["email"],
            admin_user["first_name"],
            admin_user["last_name"],
            admin_user["phone_number"],
            admin_user["password"]
        )
    print("Admin Added Successfully")
    
    for customer_user in customer_users:
        add_customer(
            customer_user["email"],
            customer_user["first_name"],
            customer_user["last_name"],
            customer_user["organisation"],
            customer_user["phone_number"],
            customer_user["address"],
            customer_user["postcode"],
            customer_user["password"]
        )  
    print("Customer Added Successfully")
        
    for interpreter_user in interpreter_users:
        add_interpreter(
            interpreter_user["email"],
            interpreter_user["first_name"],
            interpreter_user["last_name"],
            interpreter_user["phone_number"],
            interpreter_user["address"],
            interpreter_user["postcode"],
            interpreter_user["gender"],
            interpreter_user["password"],
            tags
        )
    print("Interpreter Added Successfully")
    for appointment in appointments:
        add_appointment(appointment["planned_start_time"],
                        appointment["planned_duration"],
                        appointment["location"]
                        )
    print("Appointments Added Successfully")
    for i in range(10):
        create_translation()
    print("Translations Added Successfully")


def add_admin(email,first_name,last_name,phone_number,password):
    a = Admin.objects.get_or_create(email=email)[0]
    a.first_name = first_name
    a.last_name = last_name
    a.phone_number = phone_number
    a.set_password(password)
    a.save()
    
def add_customer(email,first_name,last_name,organisation,phone_number,address,postcode,password):
    c = Customer.objects.get_or_create(email=email)[0]
    c.first_name = first_name
    c.last_name = last_name
    c.organisation = organisation
    c.phone_number = phone_number
    c.address = address
    c.postcode = postcode
    c.email_validated = True
    c.set_password(password)
    if random.randint(0, 1):
        c.approved = True
        c.approver = Admin.objects.order_by('first_name').first()
    c.save()
    

def add_interpreter(email,
                    first_name,
                    last_name,
                    phone_number,
                    address,
                    postcode,
                    gender,
                    password,
                    tags
                    ):
    i = Interpreter.objects.get_or_create(email=email)[0]
    i.first_name = first_name
    i.last_name = last_name
    i.phone_number = phone_number
    i.address = address
    i.postcode = postcode
    i.gender = gender
    i.set_password(password)
    for j in range(3):
        i.languages.add(Language.objects.all()[random.randint(0, Language.objects.count() - 1)])
        i.tag.add(Tag.objects.get(name=tags[random.randint(0, len(tags) - 1)]["tag"]))
    i.save()
    
def add_lang(lang):
    Language.objects.get_or_create(language_name=lang)[0]

def add_tag(tag,colour):
    t = Tag.objects.get_or_create(name=tag)[0]
    t.colour = colour
    t.save()
    
def add_appointment(planned_start_time,planned_duration,location):
    dt = datetime(*planned_start_time)
    a = Appointment.objects.create(
        location=location, 
        planned_start_time=timezone.make_aware(dt),
        planned_duration=time(planned_duration[0],planned_duration[1])
    )
    a.customer = Customer.objects.order_by('first_name').first()
    a.language = Language.objects.order_by('language_name').first()
    a.gender_preference = Gender.PREFER_NOT_TO_SAY
    a.language = Language.objects.all()[random.randint(0,Language.objects.count() - 1)]
    if random.randint(0, 1):
        a.admin = Admin.objects.all()[random.randint(0,Admin.objects.count() - 1)]
        a.interpreter = Interpreter.objects.all()[random.randint(0,Interpreter.objects.count() - 1)]
        if random.randint(0, 1):
            a.invoice_generated = True
    a.save()
    
def delete_all_models():
    Admin.objects.all().delete()
    Customer.objects.all().delete()
    Interpreter.objects.all().delete()
    Language.objects.all().delete()
    Tag.objects.all().delete()
    Appointment.objects.all().delete()
    Translation.objects.all().delete()
    
    folder = 'media/translation_documents'
    if (not os.path.exists(folder)):
        os.makedirs(folder)

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def import_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def random_filename(extension="txt"):
    filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return f"{filename}.{extension}"

def create_document():
    if not os.path.exists("media/translation_documents"):
        os.makedirs("media/translation_documents")
    
    file_path = os.path.join("media/translation_documents", random_filename())

    with open(file_path, 'w') as f:
        f.write(''.join(random.choices(string.ascii_letters + string.digits + " ", k=10000)))
    return file_path

def create_translation():
    t = Translation.objects.create(
        document=create_document(),
        word_count=random.randint(100, 1000)
    )
    t.customer = Customer.objects.order_by('first_name').first()
    t.language = Language.objects.order_by('language_name').first()
    t.language = Language.objects.all()[random.randint(0,Language.objects.count() - 1)]
    if random.randint(0, 1):
        t.admin = Admin.objects.all()[random.randint(0,Admin.objects.count() - 1)]
        t.interpreter = Interpreter.objects.all()[random.randint(0,Interpreter.objects.count() - 1)]
        if random.randint(0, 1):
            t.invoice_generated = True
    t.save()
    
    
if __name__ == '__main__':
    print('Starting population script...')
    try:
        delete_all_models()
        random.seed(123456789)
        populate()
    except Exception as e:
        delete_all_models()
        print(traceback.print_exception(e))
        print("UH OH!")
        exit(1)
    else:
        print('Done! :)')