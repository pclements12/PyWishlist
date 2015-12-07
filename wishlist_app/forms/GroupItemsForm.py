from wishlist_app.models import Item, WishlistGroup, GroupItem
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from django import forms


class GroupItemsForm(ModelForm):

    items = ModelMultipleChoiceField(queryset=Item.objects.all(), widget=CheckboxSelectMultiple, required=False)

    # Overriding __init__ here allows us to provide initial
    # data for 'items' field
    def __init__(self, *args, **kwargs):
        # We get the 'initial' keyword argument or initialize it
        # as a dict if it didn't exist.
        initial = kwargs.setdefault('initial', {})
        # The widget for a ModelMultipleChoiceField expects
        # a list of primary key for the selected data.
        user = None
        if 'instance' in kwargs and 'user' in kwargs:
            # need to set initial as the items already in the group
            initial['items'] = [grpi.item.pk for grpi in
                                GroupItem.objects.filter(group=kwargs['instance'],
                                                         item__wisher=kwargs['user']).select_related("item")]
            user = kwargs['user']
            print "Group Items Form, Initial items: %s" % initial['items']
        # model form doesn't expect user kwarg, so delete it
        del kwargs['user']
        super(ModelForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['items'].queryset = Item.objects.filter(wisher=user)

    # Overriding save allows us to process the value of 'groups' field
    def save(self, commit=True):
        # Get the saved Group instance
        group = ModelForm.save(self, True)

        # Prepare a 'save_m2m' method for the form,

        # self.save_m2m()
        # This is where we actually link the item with groups

        GroupItem.objects.filter(group=group).delete()

        group_items = []
        for item in self.cleaned_data['items']:
            print "creating intermediate groupitems[item] for %s" % item
            group_items.append(GroupItem(group=group, item=item).save())

        return group_items

    class Meta:
        model = WishlistGroup
        fields = ["creator", "name", "description", "type", "end_date"]
        widgets = {
            'creator': forms.HiddenInput(),
            'name': forms.HiddenInput(),
            'description': forms.HiddenInput(),
            'type': forms.HiddenInput(),
            'end_date': forms.HiddenInput(),
        }
