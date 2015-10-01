from django.forms import ModelForm
from wishlist_app.models import RegistryAssignment
from django.utils.translation import ugettext_lazy as _


class RegistryForm(ModelForm):

    def __init__(self, group, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['group'] = group
        kwargs['initial'] = initial
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['wisher'].queryset = group.users

    class Meta:
        model = RegistryAssignment
        fields = ["wisher"]
        labels = {
            'wisher': _(''),
        }
