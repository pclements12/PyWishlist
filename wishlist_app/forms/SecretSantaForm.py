from django.forms import ModelForm
from wishlist_app.models import SecretSantaAssignment
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory


class SecretSantaForm(ModelForm):

    def __init__(self,  *args, **kwargs):
        # set the group on the initial object
        super(ModelForm, self).__init__(*args, **kwargs)
        # filter the users by this group's users
        if self.instance and self.instance.pk:
            self.fields['giver'].queryset = self.instance.group.users
            self.fields['wisher'].widget.attrs['disabled'] = True
            self.fields['wisher'].required = False

    class Meta:
        model = SecretSantaAssignment
        fields = ["wisher", "giver"]
        labels = {
            'giver': _('Secret Santa'),
        }

SecretSantaFormSet = modelformset_factory(SecretSantaAssignment, form=SecretSantaForm, extra=0)

