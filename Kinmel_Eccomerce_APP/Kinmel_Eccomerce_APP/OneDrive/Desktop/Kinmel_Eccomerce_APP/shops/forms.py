from django import forms
from django.forms import inlineformset_factory
from .models import Shop, Product, ProductImage, Category, DiscountRequest


class ShopForm(forms.ModelForm):
    """Form for creating and editing shops"""
    
    class Meta:
        model = Shop
        fields = [
            'name', 'description', 'logo', 'banner', 'address', 
            'phone', 'email', 'website', 'opening_time', 'closing_time'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field in self.fields:
            if field not in ['logo', 'banner']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProductForm(forms.ModelForm):
    """Form for creating and editing products"""
    
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'description', 'price', 'original_price',
            'sku', 'condition', 'brand', 'model', 'stock_quantity',
            'low_stock_threshold', 'weight', 'length', 'width', 'height',
            'is_featured', 'is_digital', 'meta_title', 'meta_description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'original_price': forms.NumberInput(attrs={'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'step': '0.01'}),
            'length': forms.NumberInput(attrs={'step': '0.01'}),
            'width': forms.NumberInput(attrs={'step': '0.01'}),
            'height': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field in self.fields:
            if isinstance(self.fields[field].widget, forms.CheckboxInput):
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        original_price = cleaned_data.get('original_price')
        
        if original_price and price and original_price < price:
            raise forms.ValidationError("Original price cannot be less than current price.")
        
        return cleaned_data


class ProductImageForm(forms.ModelForm):
    """Form for product images"""
    
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_primary', 'order']
        widgets = {
            'alt_text': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Formset for handling multiple product images
ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm, extra=3, can_delete=True
)


# ReviewForm will be implemented later when Review model is added
# class ReviewForm(forms.ModelForm):
#     """Form for customer reviews"""
#     pass


class DiscountRequestForm(forms.ModelForm):
    """Form for trader discount requests"""
    
    class Meta:
        model = DiscountRequest
        fields = [
            'product', 'discount_type', 'discount_value', 'reason',
            'start_date', 'end_date'
        ]
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'discount_value': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_trader:
            # Filter products to only show trader's products
            self.fields['product'].queryset = Product.objects.filter(
                shop__owner=user, is_active=True
            )
        
        # Add CSS classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        discount_type = cleaned_data.get('discount_type')
        discount_value = cleaned_data.get('discount_value')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        if discount_type == 'percentage' and discount_value and discount_value > 100:
            raise forms.ValidationError("Percentage discount cannot exceed 100%.")
        
        return cleaned_data


# PromoCodeForm will be implemented later
# class PromoCodeForm(forms.ModelForm):
#     """Form for admin promo code creation"""
#     pass
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'discount_value': forms.NumberInput(attrs={'step': '0.01'}),
            'minimum_order_amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes
        for field in self.fields:
            if isinstance(self.fields[field].widget, forms.CheckboxInput):
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        discount_type = cleaned_data.get('discount_type')
        discount_value = cleaned_data.get('discount_value')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        if discount_type == 'percentage' and discount_value and discount_value > 100:
            raise forms.ValidationError("Percentage discount cannot exceed 100%.")
        
        return cleaned_data


class ProductSearchForm(forms.Form):
    """Form for product search and filtering"""
    query = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price',
            'step': '0.01'
        })
    )
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price',
            'step': '0.01'
        })
    )
    condition = forms.ChoiceField(
        choices=[('', 'Any Condition')] + Product.CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    in_stock_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
