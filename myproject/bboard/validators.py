from django.core.exceptions import ValidationError

class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
    
    # !!! ДОБАВЛЕНИЕ МЕТОДА DECONSTRUCT !!!
    def deconstruct(self):
        # path - полный путь к классу (например, 'bboard.validators.MinMaxValueValidator')
        path = 'bboard.validators.MinMaxValueValidator' 
        
        # args - позиционные аргументы (их нет)
        args = () 
        
        # kwargs - именованные аргументы, которые будут записаны в файл миграции
        kwargs = {
            'min_value': self.min_value,
            'max_value': self.max_value,
        }
        return path, args, kwargs
    # !!! КОНЕЦ ДОБАВЛЕНИЯ !!!

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введенное число должно ' + \
                                  'находиться в диапазоне от %(min)s до %(max)s', 
                                  code='out_of_range', 
                                  params={'min': self.min_value, 'max': self.max_value})

# Функция-валидатор (она сериализуется автоматически, deconstruct не нужен)
def validate_positive(value):
    if value < 0:
        raise ValidationError(
            'Значение %(value)s не может быть отрицательным.',
            code='negative_value',
            params={'value': value},
        )