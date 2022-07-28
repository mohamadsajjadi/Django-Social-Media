from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms


class RegisterView(View):
    form_classes = forms.UserRegistrationForm
    templates_name = 'account/register.html'

    def get(self, request):
        form = self.form_classes()
        return render(request, self.templates_name, {"form": form})

    def post(self, request):
        form = self.form_classes(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            messages.success(request, 'you registered succefully', 'success')
            return redirect('home:home')
        return render(request, self.templates_name, {"form": form})
