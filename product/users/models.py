from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Course


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )
    subscriptions = models.ManyToManyField(
        "courses.Course",
        through="Subscription"
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя. задание 4"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='balance',
    )
    amount = models.PositiveIntegerField(
        default=1000
    )
    # TODO

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def __str__(self):
        return f"Balance for {self.user.username}: {self.amount}"


class Subscription(models.Model):
    """Модель подписки пользователя на курс. задание 2?"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    purchase_date = models.DateTimeField(
        auto_now=True
    )
    # TODO

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
