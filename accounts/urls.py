from django.urls import path, reverse_lazy
from django.contrib.auth.views import ( 
    LogoutView,
    PasswordResetView, 
    PasswordChangeView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . views import (
    SignUpView, ProfileView, ActivateAccount, CustomLoginView,
    ApiSignUpView, ApiLogInView
)
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'accounts'

urlpatterns = [
    path('api-signup/', ApiSignUpView.as_view(), name='api_sign_up'),
    path('api-login/', ApiLogInView.as_view(), name='api_log_in'),
    path('login/', CustomLoginView.as_view(
        redirect_authenticated_user=True, template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<uuid:pk>/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    path('change-password/',
        PasswordChangeView.as_view(
            template_name='registration/change-password.html',
            success_url = reverse_lazy('quiz:start_page')
        ),
        name='change_password'),

    path('password-reset/',
        PasswordResetView.as_view(
            template_name='registration/password-reset/password_reset.html',
            subject_template_name='registration/password-reset/password_reset_subject.txt',
            email_template_name='registration/password-reset/password_reset_email.html',
            success_url = reverse_lazy('accounts:login')
        ),
        name='password_reset'),

    path('password-reset/done/',
        PasswordResetDoneView.as_view(
            template_name='registration/password-reset/password_reset_done.html'
        ),
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='registration/password-reset/password_reset_confirm.html',
            success_url = reverse_lazy('accounts:login')
        ),
        name='password_reset_confirm'),

    path('password-reset-complete/',
        PasswordResetCompleteView.as_view(
            template_name='registration/password-reset/password_reset_complete.html'
        ),
        name='password_reset_complete'),
]