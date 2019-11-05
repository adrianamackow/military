from django import forms
from .models import Warehouse


class WarehouseForm(forms.ModelForm):

    class Meta:
        model = Warehouse
        fields = ('name', 'how_many', 'priority', 'min', 'max', 'weight')
