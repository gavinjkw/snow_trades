# forms.py 
from django import forms 
from .models import *
  
class ItemForm(forms.ModelForm): 
  
    class Meta: 
        model = Item 
        fields = ['make', 'model', 'desc', 'price', 'category', 'size', 'condition', 'created_at', 'updated_at', 'added_by', 'image_one', 'image_two', 'image_three']