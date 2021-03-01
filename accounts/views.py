from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from . forms import SignUpForm, ProfileForm
from . models import CustomUser
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from . tokens import account_activation_token


class SignUpView(View):
    '''This is the signup view with renders the signup template'''
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Kindly activate Your Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('accounts:login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):
    '''This is a function to confirm the user email, if email is not confirmed he has no access to the account'''
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('quiz:home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly it has already been used.'))
            return redirect('quiz:home')



class ProfileView(UpdateView):
    '''This is to update the users details'''
    model = CustomUser
    form_class = ProfileForm
    success_url = reverse_lazy('quiz:home')
    template_name = 'registration/profile.html'