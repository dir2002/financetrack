from django import forms
import datetime
from django.forms import (CharField, DateField, DateInput, DecimalField, Textarea, 
                          ModelChoiceField, ModelForm, NumberInput, Select, TextInput, Form, ValidationError)

from .models import SubCategory, Category

from .models import BudgetLimit
class BudgetLimitForm(forms.ModelForm):
    category = ModelChoiceField(queryset=Category.objects.all(), label='', empty_label="Выберите категорию", required=True, widget=Select(attrs={'class': 'form-control'}))
    subcategory = ModelChoiceField(queryset=SubCategory.objects.all(), label='', empty_label="Выберите подкатегорию", required=True, widget=Select(attrs={'class': 'form-control'}))
    limit_amount = DecimalField(max_digits=12, decimal_places=2, required=True, label='', widget=NumberInput(attrs={'placeholder': 'Введите сумму статьи', 'class': 'form-control'}))
    start_date = DateField(label='Дата начала периода', required=True, widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = DateField(label='Дата завершения периода', required=True, widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}))
   
    class Meta:
        model = BudgetLimit
        fields = ['category', 'subcategory', 'limit_amount', 'start_date', 'end_date']
         

class BudgetLimitUpdateForm(ModelForm):
    class Meta:
        model = BudgetLimit
        fields = ['category', 'subcategory', 'limit_amount', 'start_date', 'end_date']
        widgets = {
            'date': DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),}
        
       # необходимые проверки на принадлежность подкатегории выбранной категории, сегодняшней дате, отрицательной суммы
    def clean_subcategory(self):
        subcategory = self.cleaned_data.get("subcategory")
        category = self.cleaned_data.get("category")
        if subcategory and category and subcategory.category != category: 
            raise ValidationError("Выбранная подкатегория не принадлежит указанной категории.")
        return subcategory
    
    def clean_limit_amount(self):
        limit_amount = self.cleaned_data.get("limit_amount")
        if limit_amount < 0:
            raise ValidationError("Сумма статьи не может быть отрицательной.")
        return limit_amount
    
   