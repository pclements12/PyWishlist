from wishlist_app.models import WishlistGroup
from django.forms import ModelForm


class GroupForm(ModelForm):
    class Meta:
        model = WishlistGroup
        fields = ["name", "description", "end_date"]

