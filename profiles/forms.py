from .models import Profile
from django.forms import ModelForm
from django import forms


class EditProfile(ModelForm):
    class Meta:
        model = Profile
        fields = ["location", "user_type", "specialization", "work_experience"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(EditProfile, self).__init__(*args, **kwargs)
        if user:
            self.fields["username"] = forms.CharField(initial=user.username)
            self.fields["first_name"] = forms.CharField(initial=user.first_name)
            self.fields["last_name"] = forms.CharField(initial=user.last_name)

    def save(self, commit=True):
        profile = super(EditProfile, self).save(commit=False)
        if commit:
            profile.save()
        return profile