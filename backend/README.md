# Project Architecture
![Project Architecture](/docs/Platform%20Architecture.jpeg)

# Project Structure
```
backend/            # Main backend directory
|-- asgi.py         # ASGI configuration for asynchronous server support
|-- __init__.py     # Package initialization
|-- settings.py     # Django project settings
|-- urls.py         # URL routing configuration
|-- wsgi.py         # WSGI configuration for deployment

bookingandbilling/  # Main application handling booking and billing
|-- admin.py        # Admin panel configuration
|-- apps.py         # App configuration
|-- email_utils.py  # Utilities for sending emails
|-- forms.py        # Form handling
|-- __init__.py     # Package initialization
|-- middleware.py   # Custom middleware for request handling
|-- migrations/     # Database migrations directory
|-- models.py       # Database models definition
|-- permissions.py  # Custom permissions for API access
|-- serializers/    # Serializers for API requests/responses
|   |-- appointment_serializers.py  # Appointment-related serializers
|   |-- authentication_serializers.py  # Authentication-related serializers
|   |-- edit_user_serializers.py  # Serializers for editing user data
|   |-- model_serializers.py  # General model serializers
|   |-- registration_serializers.py  # Registration-related serializers
|   |-- translation_serializers.py  # Translation-related serializers
|-- tests/          # Unit tests
|   |-- test_admin_appointments.py  # Tests for admin appointment handling
|   |-- test_admin_translations.py  # Tests for translation admin functions
|   |-- test_appointments.py  # Tests for appointment handling
|   |-- test_authentication.py  # Tests for authentication system
|   |-- test_email_validation.py  # Tests for email validation
|   |-- test_miscellaneous.py  # Miscellaneous tests
|   |-- test_models.py  # Tests for models
|   |-- test_profile_edit.py  # Tests for profile edit functionality
|   |-- test_registration.py  # Tests for user registration
|   |-- test_translations.py  # Tests for translation features
|   |-- tests_emails.py  # Tests related to email handling
|-- tokens.py       # Token-based authentication handling
|-- urls.py         # URL routing for booking and billing
|-- utilities.py    # Miscellaneous utility functions
|-- views/          # Views handling API logic
|   |-- views_appointments.py  # Appointment-related views
|   |-- views_authentication.py  # Authentication-related views
|   |-- views_registration.py  # User registration views
|   |-- views_translations.py  # Translation-related views
|   |-- views_user_edit.py  # Views for user profile editing
|   |-- views_utility.py  # Miscellaneous utility views

Dockerfile          # Docker configuration for containerization
manage.py          # Django management script
media/             # Media files (e.g., uploaded documents)
|-- translation_documents/  # Folder for storing translation-related documents

populate.py        # Script for populating database with dummy data
populateJSONs/     # JSON files containing sample data
|-- admin.json         # Sample admin data
|-- appointments.json  # Sample appointments data
|-- customer.json      # Sample customer data
|-- interpreter.json   # Sample interpreter data
|-- lang.json          # Sample language data
|-- tags.json          # Sample tags data

README.md          # Project documentation
requirements.txt   # Python dependencies
static/            # Static files (CSS, JS, images, etc.)
staticfiles/       # Collected static files after running `collectstatic`
templates/         # HTML templates for email notifications
|-- user/
    |-- appointment_accepted_email.html  # Email template for accepted appointments
    |-- appointment_offered_email.html   # Email template for offered appointments
    |-- password_reset_email.html        # Email template for password reset
    |-- verification_email.html          # Email template for account verification
```

# Installation & Setup
The majority of the setup is taken care of by Docker however, Django still requires several
environment which include:
- POSTGRES_DB - The name of the database
- POSTGRES_USER - The username Django will use to access the database.
- POSTGRES_PASSWORD - The password Django will use to access the database.
- POSTGRES_HOST - The host the database is running on, that is the docker container.
- POSTGRES_PORT - The port number that the database is accepting connections to.
- DJANGO_SECRET_KEY - The secret key that should be securely generated as it is used for encryption in django.
- DJANGO_DEBUG - Debug boolean
- DJANGO_ALLOWED_HOSTS - The host names/ip address which the application is permitted to run on.
- EMAIL_HOST_USER - The email which will send the notifications from the system.
- EMAIL_HOST_PASSWORD - The password/app password associated with the above email.
- DEFAULT_FROM_EMAIL - The from field in the email, that is what the reciever will see.


# Database Configuration
Django provides a very simple way to interchange between different databases.
The current configuration is as follows.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': os.getenv("POSTGRES_PORT"),
    }
}
```
To change to a different database simply swap the `Engine` value to your preferred database.

# API Documentation

| **Endpoint**                                  | **Method** | **Input**                                                              | **Success Response**                                       | **Error Cases**                                                  |
|-----------------------------------------------|------------|------------------------------------------------------------------------|------------------------------------------------------------|------------------------------------------------------------------|
| **Authentication API Endpoints**              |            |                                                                        |                                                            |                                                                  |
| `/api/check-auth`                                 | `GET`      | Reads `authToken` from cookies                                         | `{ "message": ..., "account_type": ... }` | N/A                                                              |
| `/api/login`                                      | `POST`     | `{ "email": ..., "password": ... }` | `{ "token": ..., "user": { ... }, "account_type": ... }` | `403 Forbidden`, `400 Bad Request - Input errors` |
| `/api/logout`                                     | `POST`     | Reads `authToken` from cookies                                         | `{ "message": ... }`                 | `404 Not Found - Token does not exist or is already logged out`    |
| **Booking and Billing API Endpoints**         |            |                                                                        |                                                            |                                                                  |
| `/api/fetch-appointments`                         | `POST`     | `{ "unassigned": ... }`                                           | List of appointments                                       | `400 Bad Request - Assignment state not specified`               |
| `/api/offered-appointments`                       | `POST`     | Reads `authToken` from cookies                                         | List of offered appointments                               | Internal error                                                   |
| `/api/all-interpreters`                           | `GET`      | None                                                                   | List of interpreters                                       | Internal error                                                   |
| `/api/appointment-request`                        | `POST`     | Appointment details                                                    | `{ "message": ... }`     | `400 Bad Request - Input errors`                                 |
| `/api/appointments`                               | `GET`      | Reads `authToken` from cookies                                         | List of user's appointments                                | Internal error                                                   |
| `/api/appointment-acceptance/{id}`                | `POST`     | `{ "accepted": ... }`                                             | `{ "message": ... }`             | `404 Not Found - Appointment not found`                          |
| `/api/update-appointment-offering`                | `POST`     | `{ "appID": ..., "interpreterID": ..., "offer": ... }`                | `{ "message": ... }`           | `400 Bad Request - Errors in offering appointment`               |
| `/api/update-interpreter-offering`                | `POST`     | `{ "appID": ..., "accepted": ... }`                                 | `{ "message": ... }`         | `400 Bad Request - Errors in appointment acceptance`             |
| `/api/accepted-appointments`                      | `GET`      | Reads `authToken` from cookies                                         | List of accepted appointments                              | Internal error                                                   |
| `/api/edit-appointments`                          | `POST`     | `{ "appID": ..., "appActualStartTime": ..., "appActualDuration": ... }` | `{ "message": ... }`         | `400 Bad Request - Errors in appointment editing`                |
| `/api/toggle-appointment-invoice`                 | `POST`     | `{ "appID": ... }`                                                       | `{ "message": ... }`  | `400 Bad Request - Errors in toggling appointment invoice`       |
| **Account/Registration API Endpoints**        |            |                                                                        |                                                            |                                                                  |
| `/api/account-acceptance/`                    | `POST`     | `{ "email": ..., "accepted": ... }`                    | `{ "message": ... }` | `400 Bad Request` (Missing email or acceptance), `500 Internal Server Error` |
| `/api/account-request-feed/`                  | `GET`      | None                                                                   | `{ "customers": [{ "first_name": ..., "email": ..., ... }] }` | `500 Internal Server Error`                                      |
| `/api/register-admin/`                        | `POST`     | `{ "type": ..., "email": ..., "password": ... }`  | `{ "user": { ... }, "token": ... }`                    | `400 Bad Request` (Invalid type, input errors), `500 Internal Server Error` |
| `/api/register-customer/`                     | `POST`     | `{ "email": ..., "password": ... }`              | `{ "user": { ... }, "token": ... }`                    | `400 Bad Request` (Input errors), `500 Internal Server Error`      |
| `/api/check-email-validation/<uidb64>/<token>/`| `GET`      | None                                                                   | `Thank you for verifying your email!`                      | `400 Bad Request` (Invalid token), `500 Internal Server Error`     |
| `/api/send-password-reset/`                   | `POST`     | `{ "email": ... }`                                      | `{ "message": ... }` | `400 Bad Request` (Missing email), `404 Not Found` (User does not exist), `500 Internal Server Error` |
| `/api/resend-email-verification/`             | `POST`     | `{ "email": ... }`                                      | `{ "message": ... }`| `400 Bad Request` (Missing email), `404 Not Found` (User not found)  |
| `/api/new-password-validation/<uidb64>/<token>/`| `GET`      | None                                                                   | Redirects to frontend password reset page                | `400 Bad Request` (Invalid token), `500 Internal Server Error`     |
| `/api/update-password/`                       | `POST`     | `{ "uidb64": ..., "token": ..., "password": ... }` | `{ "message": ... }`         | `400 Bad Request` (Invalid token), `500 Internal Server Error`     |
| **Translation API Endpoints**                 |            |                                                                        |                                                            |                                                                  |
| `/api/unassigned-translations/`               | `GET`      | None                                                                   | `{ "translations": [...] }`                                | `500 Internal Server Error`                                      |
| `/api/fetch-translations/`                    | `POST`     | `{ "unassigned": ... }`                                         | `[ { "id": ..., "document": ..., "customer": ..., interpreter: ..., "word_count": ..., "language": ..., "company": ... }, ... ]` | `400 Bad Request` (Missing "unassigned" field), `500 Internal Server Error` |
| `/api/translation-request/`                   | `POST`     | `{ "document": ..., "document_name": ..., ... }`   | `{ "message": ... }`   | `400 Bad Request` (Invalid input), `500 Internal Server Error`     |
| `/api/translations/`                          | `GET`      | None                                                                   | `{ "result": [...] }`                                      | `500 Internal Server Error`                                      |
| `/api/offered-translations/`                  | `POST`     | None (authToken in cookies)                                            | `[ { "pk": ..., "document": ..., ... }, ... ]`             | `500 Internal Server Error`                                      |
| `/api/translation-offering-response/`         | `POST`     | `{ "translationID": ..., "accepted": ... }`                       | `{ "message": ... }`       | `400 Bad Request` (Invalid translationID or missing fields), `500 Internal Server Error` |
| `/api/translation-acceptance/<id>/`           | `POST`     | `{ "accepted": ... }`                                           | `{ "message": ... }`           | `404 Not Found` (Translation not found), `500 Internal Server Error` |
| `/api/update-translation-offering/`           | `POST`     | `{ "translationID": ..., "interpreterID": ..., "offer": ... }`      | `{ "message": ... }`         | `400 Bad Request` (Invalid IDs or input), `500 Internal Server Error` |
| `/api/toggle-translation-invoice/`            | `POST`     | `{ "translationID": ... }`                                               | `{ "message": ... }`  | `400 Bad Request` (Invalid translationID), `500 Internal Server Error` |
| `/api/fetch-interpreter-accepted-translations/`| `POST`     | None (authToken in cookies)                                            | `[ { "pk": ..., "document": ..., ... }, ... ]`             | `500 Internal Server Error`                                      |
| `/api/set-translation-actual-word-count/`     | `POST`     | `{ "translationID": ..., "actualWordCount": ... }`                       | `{ "message": ... }`       | `400 Bad Request` (Invalid translationID), `500 Internal Server Error` |
| **User Edit API Endpoints**                   |            |                                                                        |                                                            |                                                                  |
| `/api/retrieve-emails/`                           | `GET`      | None                                                                   | List of emails categorized by user type                  | Internal server error                                            |
| `/api/get-user-edit-fields/`                      | `GET`      | `user` (optional, defaults to self)                                    | Editable fields for the specified user                   | User not found, Not admin, Unknown user type                     |
| `/api/edit-user/`                                 | `POST`     | `user` (optional, defaults to self), Form data                         | Updated user information                                 | User not found, Not admin, Form errors, Incorrect password         |
| `/api/admin-edit-other/`                          | `POST`     | `target-user`, Form data                                               | Updated user information                                 | Not admin, User not found, Form errors                           |
| **Languages API Endpoints**                   |            |                                                                        |                                                            |                                                                  |
| `/api/retrieve-languages/`                        | `GET`      | None                                                                   | List of available languages                              | Internal server error                                            |



# Authentication & Authorization

### Overview
Django Rest Framework (DRF) has been set up to use token authentication. By default, API views require a user to be logged in to access them. When a user logs in, a token is generated and stored for the account being accessed. This token is both stored on the backend and provided to the client. The token provided to the client is stored in an HTTP-Only cookie. This cookie:

- Exists for 1 day and persists between sessions.
- Is automatically attached to all API calls made using the `axios` API client.
- Is HTTP-Only, preventing direct JavaScript access (protecting against XSS attacks).

When a user logs out, both the cookie and the backend-stored token are deleted.

The default DRF token authentication method requires the `authToken` to be attached to requests as a header, not as a cookie. This behavior has been overridden in `backend/bookingandbilling/middleware.py` and referenced in `settings.py`.

### Calling an API Endpoint

An API endpoint must be defined in `backend/bookingandbilling/urls.py` before being accessible. It can then be called like normal by the client.

### Make API Endpoints Require / Not Require Login

By default, all API endpoints require a valid `authToken`. This is automatically handled by the API client if a token exists.

To allow access for unauthenticated users, add the following to the top of the endpoint:

```python
permission_classes = [AllowAny]
```

### Check the User Type Calling an Endpoint

The request's `authToken` can be accessed using:

```python
token = request.COOKIES.get('authToken')
```

The associated User model can be retrieved using:

```python
user = get_user_from_token(token)
```

If `token` is `None` or no associated user is found, `None` is returned.

To retrieve the high-level user type, use:

```python
user, user_type = get_full_user(user)
```

This returns:
- The high-level user (Admin, Interpreter, or Customer).
- The type as an `AccountType` ENUM value.

### Restrict an API to Specific User Types

To restrict an API to certain user types, use the custom permission class:

```python
permission_classes = [lambda: IsUserType(allowed_types=[AccountType.ADMIN, AccountType.CUSTOMER])]
```

Modify the `allowed_types` list to include any `AccountType` ENUM values that should have access.



# Testing

Django provides a powerful built-in testing framework that allows developers to write unit and integration tests for their applications. Using Django’s test suite alongside **Coverage.py** helps ensure that all critical code paths are tested while identifying untested parts of the codebase.  

### **1. Setting Up Django Tests**  
Django’s testing framework is based on **Python’s unittest module** and provides additional utilities for handling database interactions, HTTP requests, and authentication.  

To begin writing tests, ensure your Django app is properly set up for testing by adding a `tests.py` file inside each app or creating a `tests` directory with multiple test files.  

### **2. Writing Django Tests**  
Django test cases should extend `django.test.TestCase`, which provides built-in database rollback, test clients, and assertions. See the current test suite as examples.

### **3. Running Django Tests**  
To run your test suite, use the following command:  
```sh
python manage.py test <path-to-test-directory>
```
Django will automatically discover test cases inside `tests.py` files or `tests/` directories in each app.  

### **4. Using Coverage.py for Test Coverage**  
To measure how much of your code is covered by tests, install **Coverage.py**:  
```sh
pip install coverage
```
Then, run tests with coverage tracking:  
```sh
coverage run manage.py test
```
After the tests complete, generate a coverage report:  
```sh
coverage report -m
```
For an HTML report with a detailed visual breakdown:  
```sh
coverage html
```
Then open `htmlcov/index.html` in a browser to explore coverage statistics.  

### **5. Best Practices for Django Testing**  
- Use **setUp** and **tearDown** methods to create reusable test data.  
- Mock external API calls using **unittest.mock** or **responses**.  
- Write **unit tests** for models, views, and serializers, and **integration tests** for workflows.  
- Run tests in CI/CD pipelines to ensure new code does not break functionality.  

By combining Django’s built-in test framework with **Coverage.py**, you can improve code quality, catch potential bugs, and ensure your API behaves as expected across different scenarios.  
