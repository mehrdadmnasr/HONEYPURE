from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_name', 'address_details', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'phone_number', 'mobile_number', 'email', 'location_lat', 'location_long', 'default']
        widgets = {
            'address_details': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # کاربر را از ویو دریافت می‌کنیم
        super(AddressForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        address = super().save(commit=False)
        address.user = self.user  # تنظیم کاربر به عنوان صاحب آدرس
        if commit:
            address.save()
        return address

    def clean_address_name(self):
        address_name = self.cleaned_data.get('address_name')
        # بررسی وجود آدرس با همان نام برای کاربر
        if Address.objects.filter(user=self.user, address_name=address_name).exists():
            raise forms.ValidationError("An address with this name already exists for this user.")
        return address_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if mobile_number and not mobile_number.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")
        return mobile_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                forms.EmailField().clean(email)
            except forms.ValidationError:
                raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        address_name = cleaned_data.get('address_name')
        address_line1 = cleaned_data.get('address_line1')
        city = cleaned_data.get('city')
        postal_code = cleaned_data.get('postal_code')
        country = cleaned_data.get('country')
        mobile_number = cleaned_data.get('mobile_number')
        location_lat = cleaned_data.get('location_lat')
        location_long = cleaned_data.get('location_long')

        # Ensure that required fields are not empty
        if not address_name:
            self.add_error('address_name', 'Address name is required.')
        if not address_line1:
            self.add_error('address_line1', 'Address line 1 is required.')
        if not city:
            self.add_error('city', 'City is required.')
        if not postal_code:
            self.add_error('postal_code', 'Postal code is required.')
        if not country:
            self.add_error('country', 'Country is required.')
        if not mobile_number:
            self.add_error('mobile_number', 'Mobile number is required.')
        if not location_lat:
            self.add_error('location_lat', 'Latitude is required.')
        if not location_long:
            self.add_error('location_long', 'Longitude is required.')

        return cleaned_data
