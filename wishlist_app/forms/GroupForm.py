from wishlist_app.models import WishlistGroup, SecretSantaAssignment, RegistryAssignment
from django.forms import ModelForm, DateInput


class GroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # leave type empty and not required on an update
            self.fields['type'].required = False
            self.fields['type'].widget.attrs['disabled'] = True

    # ensure that type's never updated maliciously (not just through the form)
    def clean_type(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.type
        else:
            return self.cleaned_data['type']

    class Meta:
        model = WishlistGroup
        fields = ["name", "description", "type", "end_date"]
        widgets = {
            'end_date': DateInput(attrs={'type': 'date'})
        }
