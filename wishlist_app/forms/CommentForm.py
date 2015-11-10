from wishlist_app.models import Comment
from django.forms import ModelForm
from django import forms


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ["text", "anonymous"]
        labels = {
            'text': "Add Comment",
            'anonymous': "Post comment anonymously"
        }
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': 'enter comment text...'}),
        }
