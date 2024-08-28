from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import serializers
from courses.models import Course, Group, Lesson
from users.models import Subscription

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    # TODO Доп. задание

    course = serializers.StringRelatedField(read_only=True)
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['name', 'course', 'students']


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()
        # TODO Доп. задание

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        total_students_by_available_seats = (
            obj.groups.aggregate(
                total_students=Sum('max_students') - Sum('available_seats')
            )['total_students'] or 0
        )
        return total_students_by_available_seats
        # TODO Доп. задание

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел.."""
        groups = obj.groups.all()
        total_seats = sum(group.available_seats for group in groups)
        occupied_seats = sum(
            group.available_seats - group.students.count() for group in groups
        )
        if total_seats == 0:
            return 0
        return (occupied_seats / total_seats) * 100
        # TODO Доп. задание

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        total_users = User.objects.count()
        course_subscriptions = Subscription.objects.filter(course=obj).count()
        if total_users == 0 or course_subscriptions == 0:
            return 0
        return (course_subscriptions / total_users) * 100
        # TODO Доп. задание

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'cost',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
            'availability'
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = (
            'author',
            'title',
            'start_date',
            'cost',)
