from django.db import models
from django.contrib.auth import get_user_model


class Course(models.Model):
    """Модель продукта - курса. задание 1.1 готово"""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    cost = models.PositiveIntegerField(default=1000)
    availability = models.BooleanField(
        default=True
    )
    # TODO

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока. задание 1.3"""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    # TODO

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    name = models.CharField(
        max_length=100
    )
    max_students = models.IntegerField(
        default=30
    )
    available_seats = models.IntegerField(
        default=30
    )
    students = models.ManyToManyField(
        get_user_model(),
        through='GroupMembership',
        related_name='students_groups',
        blank=True
    )

    def __str__(self):
        return f"{self.course.name} - {self.name}"
    # TODO

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)


class GroupMembership(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'group')
        verbose_name = 'Членство в группе'
        verbose_name_plural = 'Членства в группах'

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"
