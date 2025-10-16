from django import forms
from .models import Xuser, Tweet


class ProfileCompletionForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False)
    display_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your Display Name"}),
    )
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "Write a short bio (max 160 characters)"}
        ),
        max_length=160,
        required=False,
    )

    class Meta:
        model = Xuser
        fields = ["profile_photo", "display_name", "bio"]


class TweetForm(forms.ModelForm):

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "What's happening",
                "maxlength": 280,
                "class": "w-full  resize-none bg-black text-white text-xl focus:outline-none placeholder-gray-500 pt-3",
            }
        ),
        max_length=280,
        required=False,
        label=False,
    )
    image = forms.ImageField(required=False, label=False)

    class Meta:
        model = Tweet
        fields = ["content", "image"]



class ProfileEditForm(forms.ModelForm):

    profile_photo = forms.ImageField(required=False, label="Change Profile Photo")
    

    delete_photo = forms.BooleanField(required=False, label="Delete Profile Photo")

    display_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "...", "placeholder": "Display Name"}),
    )
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "class": "...", "placeholder": "Write a short bio (max 160 characters)"}
        ),
        max_length=160,
        required=False,
    )

    class Meta:
        model = Xuser
       
        fields = ["profile_photo", "display_name", "bio"]