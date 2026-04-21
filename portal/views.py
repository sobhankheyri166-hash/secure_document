from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_POST
from django.views.generic import ListView, UpdateView, CreateView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Max
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import StaffRequestCreator, CustomerProfileEditForm, CustomerCreationForm
from .models import User, Request

# METHODS
def staff_check(user):
    return user.is_staff

@login_required
@user_passes_test(staff_check)
@require_POST
def customer_delete(request,customer_username):
    customer_to_delete = get_object_or_404(User,username=customer_username)
    customer_to_delete.delete()
    return redirect('customers_list')


class StaffWorkspaceView(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request):
        customers_having_request = User.objects.filter(is_staff=False,file_request__isnull=False).distinct()
        if customers_having_request.exists():
            context = customers_having_request.annotate(total_requests=Count('file_request'),
                                                last_request=Max('file_request__date_created')).order_by('-last_request')
            return render(request,'portal/workspace.html',{'context':context})
        return render(request,'portal/workspace.html',{'text':'You Have Made No Requests Yet!'})
    
    def test_func(self):
        return self.request.user.is_staff


class NewRequestView(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request):
        form = StaffRequestCreator()
        return render(request,'portal/new_request_creation.html',{'form':form})
    
    def post(self,request):
        form = StaffRequestCreator(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request,'Request sent Successfully')
            return redirect('new_request')
        messages.error(request,"An Error Occured!")
        return redirect('new_request')
    
    def test_func(self):
        return self.request.user.is_staff
    
class EditRequestView(LoginRequiredMixin,UserPassesTestMixin,View):
    def get_obj(self):
        return get_object_or_404(Request,pk=self.kwargs.get('request_id'))
    
    def get(self,request,*args,**kwargs):
        target_obj = self.get_obj()
        form = StaffRequestCreator(hide_user_field=True,instance=target_obj)
        return render(request,'portal/customer_request_edit.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        target_obj = self.get_obj()
        form = StaffRequestCreator(request.POST, hide_user_field=True, instance=target_obj)
        if form.is_valid():
            form.save()
        return redirect('customer_requests_hub', customer_username=self.kwargs.get('customer_username'))
    
    def test_func(self):
        return self.request.user.is_staff

class CustomerRequestsHub(View,LoginRequiredMixin,UserPassesTestMixin):
    def get_user(self):
        return get_object_or_404(User,username=self.kwargs.get('customer_username'))
    
    def get(self,request,*args,**kwargs):
        target_user = self.get_user()
        target_user_request = Request.objects.filter(user=target_user)
        context = target_user_request.order_by('-last_modified')
        return render(request,'portal/customer_requests_hub.html',{'context':context})
    
    def test_func(self):
        return self.request.user.is_staff

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
    
class CustomersListView(UserPassesTestMixin,LoginRequiredMixin,ListView):
    template_name = 'portal/customers_list.html'
    context_object_name = 'users_info'

    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        return User.objects.filter(is_staff=False)
    
class CustomerProfileUpdateView(UserPassesTestMixin,LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = User
    form_class = CustomerProfileEditForm
    slug_url_kwarg = 'customer_username'
    slug_field = 'username'
    template_name = 'portal/customer_profile_edit.html'
    success_url = reverse_lazy('customers_list')
    success_message = 'Customer Profile Editted Successfully'

    def test_func(self):
        return self.request.user.is_staff
    
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
            return redirect('customers_list')
        messages.error(request,'The password you set does not meet the standards. Please type in another password.')
        return render(request,'portal/reset_password.html',{'form':form,'user':user})

class CustomerCreationView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,CreateView):
    model = User
    form_class = CustomerCreationForm
    template_name = 'portal/new_customer_creation_page.html'
    success_message = 'Customer Account Has Been Created Successfully'
    success_url = reverse_lazy('customers_list')

    def test_func(self):
        return self.request.user.is_staff


