from django.db import models

# 1. Первичная модель (сторона "один")
class Rubric(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

from django.db import models
from .validators import validate_positive, MinMaxValueValidator # Импорт валидаторов

# ... (определение Rubric)

from django.db import models
from .validators import validate_positive, MinMaxValueValidator

class Bb(models.Model):
    title = models.CharField(max_length=50) 
    content = models.TextField(null=True, blank=True)
    price = models.FloatField(
        null=True, 
        blank=True, 
        validators=[
            validate_positive,
            MinMaxValueValidator(min_value=1, max_value=1000000) 
        ]
    )
    rubric = models.ForeignKey(
        'Rubric', 
        on_delete=models.CASCADE, 
        related_name='entries'
    )
    
    # !!! ДОБАВИТЬ ЭТО ПОЛЕ !!!
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Добавление мета-класса для сортировки, который также может быть причиной ошибки, 
    # если он был в коде, но здесь не показан.
    class Meta:
        # Убедитесь, что мета-класс содержит поле 'ordering'
        ordering = ['-published'] 
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

# ... (остальные модели)

# 3. Дополнительная вторичная модель
class Comment(models.Model):
    text = models.TextField()
    
    # ForeignKey: При попытке удаления Bb, имеющего Comment, будет возбуждено исключение (models.RESTRICT) [cite: 3123]
    bb = models.ForeignKey(
        Bb, 
        on_delete=models.RESTRICT
    )
    
    def __str__(self):
        return self.text[:20] + '...'
    
    
# ... (продолжение models.py)

# 4. Модель первичная (сторона "один" для 1:1)
class UserProfile(models.Model):
    user_name = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return self.user_name

# 5. Модель вторичная (сторона "один" для 1:1)
class ProfileDetail(models.Model):
    # OneToOneField связывает две сущности 1:1 [cite: 3192, 3193]
    profile = models.OneToOneField(
        UserProfile, 
        on_delete=models.CASCADE,
        primary_key=True # Делаем OneToOneField первичным ключом для дополнительной таблицы
    )
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"Детали профиля для {self.profile.user_name}"
    
    
# ... (продолжение models.py)

# 6. Модель ведомая (Spare)
class Spare(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

# 7. Модель ведущая (Machine)
class Machine(models.Model):
    name = models.CharField(max_length=30)
    # ManyToManyField связывает множество Machine со множеством Spare [cite: 3221]
    spares = models.ManyToManyField(Spare)

    def __str__(self):
        return self.name