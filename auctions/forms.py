from django.db.models import fields
from auctions.models import Bids, Comments
from django import forms
from django.forms.widgets import HiddenInput, NumberInput
from django.forms import ModelForm
from django.db import models


CATEGORIES = (
    ('sh', 'shoe'),
    ('el', 'electronics'),
    ('cl', 'clothing'),
    ('sm', 'smartphones'),
    ('no', 'None')
)


class Create_form(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Description",widget=forms.Textarea(attrs={'rows':3}), max_length=400)
    image = forms.URLField(label="Image URL", max_length=200, error_messages = {
            'task': {'max_length': ("Error: maximum length limit is 255 characters")}
            })
    price = forms.IntegerField(label="Price")
    date_created = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    category = forms.ChoiceField(choices=CATEGORIES)

class Bid_form(forms.Form):
    bid = forms.IntegerField(label="Bid")

class Comment_form(forms.Form):
    name = forms.CharField(label="Name",max_length=80)
    email = forms.EmailField(label="Email")
    body = forms.CharField(label="Description",widget=forms.Textarea(attrs={'rows':3}), max_length=400)
    


