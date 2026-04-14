from django.db import models


class Manufacturer(models.Model):
    name = models.CharField('Название производителя', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Case(models.Model):
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name='cases',
        verbose_name='Производитель'
    )
    model_name = models.CharField('Модель корпуса', max_length=200)

    photo = models.ImageField('Основное фото', upload_to='cases_photos/')
    photo_2 = models.ImageField('Дополнительное фото 2', upload_to='cases_photos/', blank=True, null=True)
    photo_3 = models.ImageField('Дополнительное фото 3', upload_to='cases_photos/', blank=True, null=True)
    photo_4 = models.ImageField('Дополнительное фото 4', upload_to='cases_photos/', blank=True, null=True)
    photo_5 = models.ImageField('Дополнительное фото 5', upload_to='cases_photos/', blank=True, null=True)
    photo_6 = models.ImageField('Дополнительное фото 6', upload_to='cases_photos/', blank=True, null=True)

    def __str__(self):
        return f'{self.manufacturer.name} {self.model_name}'

    def all_photos(self):
        photos = [self.photo]
        if self.photo_2:
            photos.append(self.photo_2)
        if self.photo_3:
            photos.append(self.photo_3)
        if self.photo_4:
            photos.append(self.photo_4)
        if self.photo_5:
            photos.append(self.photo_5)
        if self.photo_6:
            photos.append(self.photo_6)
        return photos

    class Meta:
        verbose_name = 'Корпус'
        verbose_name_plural = 'Корпуса'


class UnknownCase(models.Model):
    photo = models.ImageField('Фото', upload_to='unknown_cases/')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return f'Неизвестный корпус #{self.id} от {self.created_at.strftime("%d.%m.%Y")}'

    class Meta:
        verbose_name = 'Неизвестный корпус'
        verbose_name_plural = 'Неизвестные корпуса'


class Message(models.Model):
    unknown_case = models.ForeignKey(UnknownCase, on_delete=models.CASCADE, related_name='messages')
    name = models.CharField('Ваше имя', max_length=100)
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return f'Сообщение от {self.name} о корпусе #{self.unknown_case.id}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
