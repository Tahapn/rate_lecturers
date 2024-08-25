from django.forms import ModelForm
from django.forms.widgets import Input
from .models import Review


class RangeInput(Input):
    input_type = 'range'


class ReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = ['rate', 'comment']
        widgets = {
            'rate': RangeInput(attrs={
                'min': 1,
                'max': 5,
                'step': 1
            })
        }
