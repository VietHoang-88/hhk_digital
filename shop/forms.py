from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    voucher_code = forms.CharField(
        required=False,
        max_length=50,
        label='Mã voucher',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mã voucher'}),
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'payment_method', 'voucher_code']
        widgets = {
            'payment_method': forms.RadioSelect,
        }

    def clean_voucher_code(self):
        code = self.cleaned_data.get('voucher_code', '').strip()
        if code and code.upper() not in ('HHK10', 'SALE100', 'SALE200'):
            raise forms.ValidationError('Mã voucher không hợp lệ')
        return code.upper()
