from django import forms
from .models import Review  # Make sure this is the correct model

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Make sure to include fields from the model
