from django import forms
from.models import *

class create_form(forms.ModelForm):
	class Meta:
		model=listing
		fields=('item_name','description','price','category_name','image','last_date')
		
		widgets = {     'item_name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'autocomplete': 'off'}),
            'price': forms.NumberInput(attrs={'autocomplete': 'off'}),
            'category_name': forms.Select(attrs={'autocomplete': 'off'}),
            'image': forms.URLInput(attrs={'autocomplete': 'off'}),
            'last_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'autocomplete': 'off'})
        }