from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Climber(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.firstname} - {self.email}'

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'


# Координаты объекта
class Coordinate(models.Model):
    latitude = models.FloatField(max_length=64, verbose_name='широта')
    longitude = models.FloatField(max_length=64, verbose_name='долгота')
    height = models.IntegerField(verbose_name='высота')

    def __str__(self):
        return f'{self.latitude},{self.longitude},{self.height}'

    class Meta:
        verbose_name = 'координат'
        verbose_name_plural = 'Координаты'


# Уровень сложности прохождения маршрута
LEVEL = [
    ('', 'не указано'),
    ('1a', '1A'),
    ('1b', '1Б'),
    ('2a', '2А'),
    ('2b', '2Б'),
    ('3a', '3А'),
    ('3b', '3Б'),
    ('4a', '4А'),
    ('4b', '4Б'),
    ('5a', '5А'),
    ('5b', '5Б'),
]


class Level(models.Model):
    winter = models.CharField(max_length=3, choices=LEVEL, verbose_name='Зима', default='')
    spring = models.CharField(max_length=3, choices=LEVEL, verbose_name='Весна', default='')
    summer = models.CharField(max_length=3, choices=LEVEL, verbose_name='Лето', default='')
    autumn = models.CharField(max_length=3, choices=LEVEL, verbose_name='Осень', default='')

    def __str__(self):
        return f'зима: {self.winter}, весна: {self.spring}, лето: {self.summer}, осень: {self.autumn}'

    class Meta:
        verbose_name = 'уровень сложности'
        verbose_name_plural = 'Уровни сложности'


# Изображения, добавленные автором
class Image(models.Model):
    title1 = models.CharField(max_length=128, verbose_name='название', blank=True)
    photo1 = models.URLField(verbose_name='фотография', blank=True)
    title2 = models.CharField(max_length=128, verbose_name='название', blank=True)
    photo2 = models.URLField(verbose_name='фотография', blank=True)
    title3 = models.CharField(max_length=128, verbose_name='название', blank=True)
    photo3 = models.URLField(verbose_name='фотография', blank=True)
    title4 = models.CharField(max_length=128, verbose_name='название', blank=True)
    photo4 = models.URLField(verbose_name='фотография', blank=True)

    #    def __str__(self):
    #       return f'{self.pk} {self.title}'

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'Фотографии'


# Информация/данные о добавленном объекте (перевале)
class Peak(models.Model):
    # Cтатус объекта
    STATUS = [
        ('new', 'новый'),
        ('pending', 'на модерации'),
        ('accepted', 'принят'),
        ('rejected', 'не принят'),
    ]

    # Активность - способ прохождения маршрута
    ACTIVITIES = [
        ('', 'не задано'),
        ('foot', 'пеший'),
        ('bike', 'велосипед'),
        ('car', 'автомобиль'),
        ('motorbike', 'мотоцикл'),
    ]

    # Категория объекта/высоты
    CATEGORY = [
        ('', 'не задано'),
        ('PA', 'перевал'),
        ('MP', 'горная вершина'),
        ('GO', 'ущелье'),
        ('PL', 'плато'),
    ]
    country = models.CharField(max_length=128, verbose_name='страна', default=None)
    category = models.CharField(max_length=3, choices=CATEGORY, default='', verbose_name='категория высоты')
    title = models.CharField(max_length=128, verbose_name='название')
    other_titles = models.CharField(max_length=128, verbose_name='другое название', blank=True)
    connect = models.TextField(default='', verbose_name='соединение')
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, verbose_name='статус', default='new')
    activities = models.CharField(max_length=64, choices=ACTIVITIES, default='', verbose_name='активность')

    user = models.ForeignKey(Climber, on_delete=models.CASCADE, default=None, verbose_name='альпенист')
    coords = models.ForeignKey(Coordinate, on_delete=models.CASCADE, verbose_name='координаты')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name='уровень сложности')
    images = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name='изображения')

    class Meta:
        verbose_name = 'вершину и перевал'
        verbose_name_plural = 'Вершины и перевалы'
