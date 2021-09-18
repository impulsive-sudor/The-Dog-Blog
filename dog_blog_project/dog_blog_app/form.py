from django import forms

class uploadprofilepicture(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()