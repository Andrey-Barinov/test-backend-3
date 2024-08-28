from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import Subscription
from .models import Course, Group, GroupMembership


@receiver(post_save, sender=Course)
def create_groups(sender, instance, created, **kwargs):
    """
    Автоматическое создание 10 пустых групп для нового курса.
    """
    # TODO
    if created:
        for i in range(10):
            Group.objects.create(
                course=instance,
                name=f"Группа {i + 1}",
                max_students=30,
                available_seats=30,
            )


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """
    # TODO
    if created:
        user = instance.user
        course = instance.course
        # Ищем самую свободную группу для данного курса
        available_group = Group.objects.filter(
            course=course,
            available_seats__gt=0
        ).order_by('-available_seats').first()

        if available_group:
            # Добавляем пользователя в группу
            GroupMembership.objects.create(user=user, group=available_group)

        else:
            # Создаем новую группу, если все существующие заполнены
            new_group_number = Group.objects.filter(course=course).count() + 1
            new_group = Group.objects.create(
                course=course,
                name=f"Group {new_group_number}",
                max_students=30,
                available_seats=30
            )
            new_group.users.add(user)
        instance.save()


@receiver(post_save, sender=GroupMembership)
@receiver(post_delete, sender=GroupMembership)
def update_available_seats(sender, instance, **kwargs):
    """
    Автоматичсекое обновление свободных мест в группах курса, с помощью
    промежуточной модели GroupMembership
    """
    # TODO
    group = instance.group
    max_students = group.max_students
    group_membership_set = group.groupmembership_set.count()
    group.available_seats = max_students - group_membership_set
    group.save()
