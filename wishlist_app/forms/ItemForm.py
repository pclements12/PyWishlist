from wishlist_app.models import Item
from django.forms import ModelForm


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "link", "quantity"]
