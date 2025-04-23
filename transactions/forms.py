import datetime
from django.forms import (CharField, DateField, DateInput, DecimalField, Textarea, 
                          ModelChoiceField, ModelForm, NumberInput, Select, TextInput, Form, ValidationError)


from .models import SubCategory, Transaction, Category, OpeningBalance


class TransactionForm(ModelForm):
    category = ModelChoiceField(queryset=Category.objects.all(), label='', empty_label="Выберите категорию", required=True, widget=Select(attrs={'class': 'form-control'}))
    subcategory = ModelChoiceField(queryset=SubCategory.objects.all(), label='', empty_label="Выберите подкатегорию", required=True, widget=Select(attrs={'class': 'form-control'}))
    amount = DecimalField(max_digits=12, decimal_places=2, required=True, label='', widget=NumberInput(attrs={'placeholder': 'Введите сумму транзакции', 'class': 'form-control'}))
    date = DateField(label='', required=False, initial=datetime.date.today, widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    description = CharField(label='', required=False, widget=TextInput(attrs={'placeholder': 'Введите краткое описание транзакции', 'class': 'form-control'}))
    
    class Meta:
        model = Transaction
        fields = ['category', 'subcategory', 'amount', 'date', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].initial = datetime.date.today().strftime('%Y-%m-%d')
        
class OpeningBalanceForm(ModelForm):
    class Meta:
        model = OpeningBalance
        exclude = ['user', 'date_saldo_update']

class TransactionUpdateForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'subcategory', 'amount', 'date', 'description']
        widgets = {
            'description': Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'date': DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),}

    # необходимые проверки на принадлежность подкатегории выбранной категории, сегодняшней дате, отрицательной суммы
    def clean_subcategory(self):
        subcategory = self.cleaned_data.get("subcategory")
        category = self.cleaned_data.get("category")
        if subcategory and category and subcategory.category != category: 
            raise ValidationError("Выбранная подкатегория не принадлежит указанной категории.")
        return subcategory
    
    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date is None:  
            raise ValidationError('Дата не может быть пустой.')
        if date > datetime.date.today():
            raise ValidationError('Дата не может быть больше текущей.')
        
        return date
    
    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount < 0:
            raise ValidationError("Сумма транзакции не может быть отрицательной.")
        return amount
    
   