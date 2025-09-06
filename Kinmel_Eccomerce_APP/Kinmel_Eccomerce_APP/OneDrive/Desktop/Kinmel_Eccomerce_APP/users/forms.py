from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, TraderProfile, CustomerProfile


class CustomUserCreationForm(UserCreationForm):
    """Base form for user registration"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 
                 'date_of_birth', 'address', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user


class CustomerRegistrationForm(CustomUserCreationForm):
    """Registration form for customers"""
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        user.is_approved = True  # Customers are auto-approved
        if commit:
            user.save()
            # Create customer profile
            CustomerProfile.objects.create(user=user)
        return user


class TraderRegistrationForm(CustomUserCreationForm):
    """Registration form for traders"""
    business_name = forms.CharField(max_length=200, required=True)
    business_license = forms.CharField(max_length=100, required=False)
    tax_id = forms.CharField(max_length=50, required=False)
    business_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    business_phone = forms.CharField(max_length=15, required=True)
    business_email = forms.EmailField(required=True)
    bank_account_number = forms.CharField(max_length=50, required=False)
    bank_name = forms.CharField(max_length=100, required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'trader'
        user.is_approved = False  # Traders need admin approval
        if commit:
            user.save()
            # Create trader profile
            TraderProfile.objects.create(
                user=user,
                business_name=self.cleaned_data['business_name'],
                business_license=self.cleaned_data['business_license'],
                tax_id=self.cleaned_data['tax_id'],
                business_address=self.cleaned_data['business_address'],
                business_phone=self.cleaned_data['business_phone'],
                business_email=self.cleaned_data['business_email'],
                bank_account_number=self.cleaned_data['bank_account_number'],
                bank_name=self.cleaned_data['bank_name'],
            )
        return user


class AdminRegistrationForm(CustomUserCreationForm):
    """Registration form for admins (restricted)"""
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'admin'
        user.is_approved = True
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with role-based validation"""
    
    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        
        # Add CSS classes for styling
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError("Invalid username or password.")
            else:
                self.confirm_login_allowed(self.user_cache)
                
                # Check role if specified
                if self.role and self.user_cache.role != self.role:
                    raise forms.ValidationError(f"This login is only for {self.role}s.")
                
                # Check if trader is approved
                if self.user_cache.role == 'trader' and not self.user_cache.is_approved:
                    raise forms.ValidationError("Your trader account is pending approval.")

        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class TraderProfileUpdateForm(forms.ModelForm):
    """Form for updating trader profile"""
    
    class Meta:
        model = TraderProfile
        fields = ['business_name', 'business_license', 'tax_id', 'business_address', 
                 'business_phone', 'business_email', 'bank_account_number', 'bank_name']
        widgets = {
            'business_address': forms.Textarea(attrs={'rows': 3}),
        }


class CustomerProfileUpdateForm(forms.ModelForm):
    """Form for updating customer profile"""
    
    class Meta:
        model = CustomerProfile
        fields = ['preferred_payment_method', 'shipping_address']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
        }
