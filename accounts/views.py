from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from events.models import Ticket
from .models import User
from .forms import RegistrationForm, LoginForm
from django.views import View


class UserRegisterView(View):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('events:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form_register': form})

    def post(self, request):
        form = self.form_class(request.POST)
        password = request.POST['password']
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('events:index')
        return render(request, self.template_name, {'form_register': form})


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('events:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form_login': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                phone_number=cd['phone_number'],
                password=cd['password'], )
            if user is not None:
                login(request, user)
                return redirect('events:index')
            return render(request, self.template_name, {'form_login': form})
        return render(request, self.template_name, {'form_login': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('events:index')


class MyTicketView(View):
    template_name = 'accounts/my-tickets.html'

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user, status=Ticket.STATUS.SUCCESSFUL)
        return render(request, self.template_name, {'ticket': tickets})
