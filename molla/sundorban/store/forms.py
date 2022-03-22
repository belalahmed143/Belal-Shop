from django import forms

class CouponCodeForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':"coupon code"
    }))

    