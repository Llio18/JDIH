
from django import forms

from .models import Kontak


# class FormKontak(forms.Form):
#     nama = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Nama',
#         })
#     )

#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Email',
#         })
#     )

#     pesan = forms.CharField(
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'Pesan',
#             'rows': '5',
#         })
#     )


class FormKontak(forms.ModelForm):
    class Meta:
        model = Kontak
        fields = ['nama', 'email', 'pesan']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),
            'pesan': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Pesan',
                'rows': 5,
            }),
        }