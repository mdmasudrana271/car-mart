from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate,login,update_session_auth_hash,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import RegisterForm  
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from carsapp.models import Order
from django.contrib.auth import login


# Create your views here.


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm 
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save() # Save the user
        login(self.request, user)
        messages.success(self.request, 'Account created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your submission.')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context



class UserLoginView(LoginView):
    template_name = 'register.html'
    # success_url = reverse_lazy('profile')
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context


@login_required
def profile(request):
    if request.user.is_authenticated:
        data = Order.objects.filter(user = request.user)
        total_price = sum(order.car.price for order in data)
        return render(request, 'profile.html', {'data':data,'user':request.user,"total":total_price})
    else:
        return redirect('user_login')
    # return render(request, 'profile.html')



@login_required
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            profile_form = forms.ChangeUserForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile Updated Successefully')
                return redirect('profile')

        else:
            profile_form = forms.ChangeUserForm(instance=request.user)
        return render(request, 'edit_profile.html', {'form':profile_form})
    else:
        return redirect('user_login')



@login_required
def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user,data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Updated Successefully')
                update_session_auth_hash(request,form.user)
                return redirect('profile')

        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'change_pass.html', {'form':form})
    else:
        return redirect('user_login')


@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('user_login')
    else:
        return redirect('user_login')
     


