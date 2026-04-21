from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import User, Request


class CustomerProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture','first_name','last_name','username','email','is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control','aria-describedby': 'profile_pict_helptext'}),
        }

class CustomerCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'profile_picture_input', 'accept': 'image/*'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name','last_name','email','profile_picture')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ('password1', 'password2'):
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class FileUpload(forms.Form):
    class Meta:
        fields = ['file','request']

class StaffRequestCreator(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['name','description','user','file_type']
        labels = {
            'name': 'Document Name (e.g. W2 Form)',
            'description': 'More about this file',
            'user': 'Select Client'
        }
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'}),
            'file_type' : forms.Select(attrs={'class':'form-select'}),
            'user' : forms.Select(attrs={'class':'form-select'})
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        hide_user_field = kwargs.pop('hide_use_field',False)
        self.fields['user'].queryset = User.objects.filter(is_staff=False)
        if hide_user_field:
            del self.fields['user']


        
        

        
