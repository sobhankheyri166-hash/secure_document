from django import forms
from .models import *


class UserManagement(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','is_active']

class FileUpload(forms.Form):
    class Meta:
        fields = ['file','request']

class StaffRequestCreator(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['name','description','user']
        labels = {
            'name': 'Document Name (e.g. W2 Form)',
            'description': 'More about this file',
            'user': 'Select Client'
        }

        
