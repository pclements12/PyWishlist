from wishlist_app.models import Item, WishlistGroup, GroupItem
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple


class ItemForm(ModelForm):

    # Representing the many to many related field in Pizza
    groups = ModelMultipleChoiceField(queryset=WishlistGroup.objects.all(), widget=CheckboxSelectMultiple)

    # Overriding __init__ here allows us to provide initial
    # data for 'groups' field
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'groups' list should be empty)
        if 'instance' in kwargs:
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['groups'] = [grp.pk for grp in kwargs['instance'].wishlistgroup_set.all()]

        ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'groups' field
    def save(self, commit=True):
        # Get the unsaved Item instance
        instance = ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def new_save_m2m():
            old_save_m2m()
            # This is where we actually link the item with groups
            instance.wishlistgroup_set.clear()
            for group in self.cleaned_data['groups']:
                print "creating intermediate groupitems for %s" % group
                GroupItem(item=instance, group=group).save()
                # instance.wishlistgroup_set.add(group)

        self.save_m2m = new_save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance

    class Meta:
        model = Item
        fields = ["name", "description", "link", "quantity"]
