from django.db import models
from django.forms import ValidationError
from users.models import User

class Category(models.Model):
    CATEGORY = [
        ('income', 'Доходы'),
        ('expense', 'Расходы'),
        ('deposit', 'Депозит'),
        ('investment', 'Инвестиции'),
        ('debt', 'Долг'),
        ]
    
    category = models.CharField('Вид операции', max_length=100, choices=CATEGORY)

    def __str__(self):
        return self.get_category_display()
    
class SubCategory(models.Model):
    SUB_CATEGORY_CHOICES = {
        'income': [
            ('salary', 'Зарплата'),
            ('deposit_income', 'Доходы от депозита'),
            ('other_income', 'Прочие поступления'),
        ],
        'expense': [
            ('Food and hygiene', 'Продукты питания и гигиена'),
            ('Clothing and footwear', 'Одежда и обувь'),
            ('Accessories', 'Аксессуары'),
            ('Sports goods and inventory', 'Спорттовары и инвентарь'),
            ('Home goods', 'Товары для дома'),
            ('Children’s goods', 'Товары для детей'),
            ('Pet supplies', 'Товары для животных'),
            ('Furniture and interior', 'Мебель и интерьер'),
            ('Electronics', 'Электроника'),
            ('Household goods', 'Хозяйственные товары'),
            ('Gifts', 'Подарки'),
            ('Books', 'Книги'),
            ('Stationery', 'Канцелярия'),
            ('Car expenses', 'Содержание автомобиля'),
            ('Other goods', 'Прочие товары'),
            ('Entertainment', 'Развлечение'),
            ('Sport', 'Спорт'),
            ('Transport services', 'Услуги транспорта'),
            ('Utilities', 'Коммунальные услуги'),
            ('Telecommunication services', 'Услуги связи'),
            ('Subscriptions and services', 'Подписки и сервисы'),
            ('Medical services and goods', 'Медицинские услуги и товары'),
            ('Preschool and educational institution services', 'Услуги учреждений детского образования'),
            ('Travel and leisure', 'Путешествия и отдых'),
            ('Cosmetology and hairdressing', 'Косметология и парикмахерская'),
            ('Education', 'Образование'),
            ('Other work and services', 'Прочие работы и услуги'),
        ],
        'deposit': [
            ('deposit_increase', 'Пополнение депозита'),
            ('deposit_decrease', 'Снятие с депозита'),
        ],
        'investment': [
            ('investment_increase', 'Приобретение инвестиций'),
            ('investment_decrease', 'Продажа инвестактивов'),
        ],
        'debt': [
            ('Increase short-term debt (up to 12 months)', 'Увеличение краткосрочного долга (до 12 месяцев)'),
            ('Decrease short-term debt (up to 12 months)', 'Уменьшение краткосрочного долга (до 12 месяцев)'),
            ('Increase long-term debt (more than 12 months)', 'Увеличение долга (более 12 месяцев)'),
            ('Decrease long-term debt (more than 12 months)', 'Уменьшение долга (более 12 месяцев)'),
        ],
    }
    subcategory = models.CharField('Тип операции', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.subcategory
    
    def clean(self):
        if self.subcategory not in [subcat[0] for subcat in self.SUB_CATEGORY_CHOICES.get(self.category.category, [])]:
            raise ValidationError(f'Неверная тип операции для {self.category}')

    
    