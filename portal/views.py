from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import SetPasswordForm
from django.views.generic import ListView, UpdateView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .models import *
from .forms import *


class LoginPortalView(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('workspace')
            return redirect('customer_dashboard')
        return render(request,'portal/login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if remember_me == 'on':
                request.session.set_expiry(200)
            else:
                request.session.set_expiry(0)
            
            if user.is_staff:
                return redirect('workspace')
            else:
                return redirect('customer_dashboard')
        
        else:
            messages.error(request,'Invalid Username or Password!')
            return redirect('login_view')
    
@login_required(login_url='login_view')
def workspace(request):
    if not request.user.is_staff:
        return redirect('login_view')
    if request.method == 'POST':
        form = StaffRequestCreator(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workspace')
    else:
        form = StaffRequestCreator()
        form.fields['user'].queryset = User.objects.filter(is_staff=False)

    return render(request,'portal/workspace.html',{'form':form})

class CustomerListView(UserPassesTestMixin,LoginRequiredMixin,ListView):
    template_name = 'portal/users_view.html'
    context_object_name = 'users_info'

    def test_func(self):
        return self.request.user.is_staff
    def get_queryset(self):
        return User.objects.filter(is_staff=False)
    
class CustomerProfileUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserManagement
    template_name = 'portal/users_dashboard.html'
    success_url = reverse_lazy('users_view')
    success_message = 'User Profile Editted Successfully'

    def test_func(self):
        return self.request.user.is_staff
    def get_user(self):
        return get_object_or_404(User,username=self.kwargs.get('customer_username'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_obj'] = self.object
        return context

class PasswordResetView(UserPassesTestMixin,LoginRequiredMixin,View):
    def test_func(self):
        return self.request.user.is_staff
    def get_user(self):
        return get_object_or_404(User,username=self.kwargs.get('customer_username'))
    def get(self,request,*args,**kwargs):
        user = self.get_user()
        form = SetPasswordForm(user)
        return render(request,'portal/reset_password.html',{'form':form,'user':user})
    def post(self,request,*args,**kwargs):
        user = self.get_user()
        form = SetPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Password was Successfully Reset')
        messages.error(request,'The password you set does not meet the standards. Please type in another password.')
        return render(request,'portal/reset_password.html',{'form':form,'user':user})

