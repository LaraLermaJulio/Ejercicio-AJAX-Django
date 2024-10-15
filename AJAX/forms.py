from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        initial="",
        required=True,
    )
    email = forms.EmailField(
        max_length=200,
        initial="",
        required=True,
    )
    message = forms.CharField(
        max_length=200,
        initial="",
        required=True,
    )
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),  # Usar ClearableFileInput
        required=False,
    )
