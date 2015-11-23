from wishlist_app.models import Comment
from django.forms import ModelForm
from django import forms


class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # leave non-updatable fields empty and not required on an update
            self.make_field_disabled('anonymous')
            self.make_field_disabled('hide_from_wisher')

    def clean_anonymous(self):
        return self.field_clean('anonymous')

    def clean_hide_from_wisher(self):
        return self.field_clean('hide_from_wisher')

    def make_field_disabled(self, field):
        self.fields[field].required = False
        self.fields[field].widget.attrs['disabled'] = True

    def field_clean(self, field):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return getattr(instance, field, None)
        else:
            return self.cleaned_data[field]

    class Meta:
        model = Comment
        fields = ["text", "anonymous", "hide_from_wisher"]
        labels = {
            'text': "Add Comment",
            'anonymous': "Post comment anonymously",
            'hide_from_wisher': "Hide comment from the wisher"
        }
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': 'enter comment text...'}),
        }
