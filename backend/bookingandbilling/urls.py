from django.urls import path
from bookingandbilling.views.views_registration import check_email_validation
from bookingandbilling.views.views_registration import new_password_validation

from .views.views_registration import (
    AccountAcceptanceView,
    AccountRequestFeedView,
    RegisterAdminViewSet,
    RegisterCustomerViewSet,
    SendPasswordResetEmail,
    UpdatePassword,
    ResendEmailVerification,
)
from .views.views_authentication import (
    LogoutView,
    LoginView,
    CheckAuthView,
)
from .views.views_utility import (
    RetrieveLanguages,
    protected_media,
)
from .views.views_appointments import (
    FetchAppointmentsView,
    AppointmentsView,
    AppointmentRequestView,
    AllInterpretersView,
    UpdateAppointmentOffering,
    ToggleAppointmentInvoiceAppView,
    OfferedAppointmentsView,
    UpdateInterpreterOffering,
    AcceptedAppointments,
    EditAppointments,
)
from .views.views_translations import (
    FetchTranslationsView,
    UpdateTranslationOffering,
    ToggleTranslationInvoiceAppView,
)
from .views.views_translations import (
    TranslationsView,
    TranslationRequestView,
    UnassignedTranslationsView,
    OfferedTranslationsView,
    TranslationOfferingResponse,
    FetchInterpreterAcceptedTranslations,
    SetTranslationActualWordCount
)


from .views.views_user_edit import (
    EditView,
    GetUserEditFieldsView,
    RetrieveEmails
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register-admin/', RegisterAdminViewSet.as_view(), name='register_admin'),
    path('register-customer/', RegisterCustomerViewSet.as_view(), name='register_customer'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('approve/', AccountAcceptanceView.as_view(), name='approve'),
    path('needs-approval/', AccountRequestFeedView.as_view(), name='needs_approval'),
    path('check-auth/', CheckAuthView.as_view(), name='check_auth'),
    path('languages/', RetrieveLanguages.as_view(), name='languages'),
    path('auth/edit_profile', EditView.as_view(), name="edit_profile"),
    path('auth/get_user_edit_fields', GetUserEditFieldsView.as_view(), name="get_user_edit_fields"),
    path('all-interpreters/', AllInterpretersView.as_view(), name='all-interpreters'),
    path('emails/', RetrieveEmails.as_view(), name='emails'),
    path('fetch-appointments/', FetchAppointmentsView.as_view(), name='fetch-appointments'),
    path('all-interpreters/', AllInterpretersView.as_view(), name='all-interpreters'),
    path('fetch-appointments/', FetchAppointmentsView.as_view(), name='fetch-appointments'),
    path('needs-approval/',CheckAuthView.as_view(), name='check_auth'),
    path('languages/', AccountRequestFeedView.as_view(), name='needs_approval'),
    path('check-auth/', RetrieveLanguages.as_view(), name='languages'),
    path('appointments/', AppointmentsView.as_view(), name="appointments-list"),
    path("appointment-request/", AppointmentRequestView.as_view(), name="appointment-request-view"),
    path('translations/', TranslationsView.as_view(), name="translations-list"),
    path("translation-request/", TranslationRequestView.as_view(), name="translation-request-view"),
    path('all-translations/', UnassignedTranslationsView.as_view(), name='all-translations'),
    path('all-interpreters/', AllInterpretersView.as_view(), name='all-interpreters'),
    path('offer-appointments/', UpdateAppointmentOffering.as_view(), name='offer-appointments'),
    path('offered-appointments/', OfferedAppointmentsView.as_view(), name='offered-appointments'),
    path('offered-translations/', OfferedTranslationsView.as_view(), name='offered-appointments'),
    path('updated-appointments/', UpdateInterpreterOffering.as_view(), name='updated-appointments'),
    path('accepted-appointments/', AcceptedAppointments.as_view(), name='accepted-appointments'),
    path('edit-appointments/', EditAppointments.as_view(), name='edit-appointments'),
    path(
        'toggle-appointment-invoice/',
        ToggleAppointmentInvoiceAppView.as_view(),
        name='toggle-appointment-invoice'
    ),
    path('fetch-translations/', FetchTranslationsView.as_view(), name='fetch-translations'),
    path('offer-translations/', UpdateTranslationOffering.as_view(), name='offer-translations'),
    path(
        'toggle-translation-invoice/',
        ToggleTranslationInvoiceAppView.as_view(),
        name='toggle-translation-invoice'
    ),
    path('offered-appointments/', OfferedAppointmentsView.as_view(), name='offered-appointments'),
    path('updated-appointments/', UpdateInterpreterOffering.as_view(), name='updated-appointments'),
    path('update-translation/', TranslationOfferingResponse.as_view(), name='updated-appointments'),
    path('accepted-appointments/', AcceptedAppointments.as_view(), name='accepted-appointments'),
    path('edit-appointments/', EditAppointments.as_view(), name='edit-appointments'),
    path(
        'send-password-reset-email/',
        SendPasswordResetEmail.as_view(),
        name='send-password-reset-email'),
    path(
        'new-password/<str:uidb64>/<str:token>/',
        new_password_validation,
        name='new-password'),
    path('validate_email/<str:uidb64>/<str:token>',
         check_email_validation,
         name='check_email_validation'),
    path('update-password/', UpdatePassword.as_view(), name='update-password'),
    path(
        'fetch-accepted-translations/',
        FetchInterpreterAcceptedTranslations.as_view(),
        name='fetch-accepted-translations'
    ),
    path(
        'set-translations-actual-word-count/',
        SetTranslationActualWordCount.as_view(),
        name='set-translations-actual-word-count'
    ),
    path(
        'resend-email-verification/',
        ResendEmailVerification.as_view(),
        name='resend-email-verification'
    ),
    path('protected-media/<path:path>/', protected_media.as_view(), name='protected_media'),
]
