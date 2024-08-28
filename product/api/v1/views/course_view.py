from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from courses.models import Course
from users.models import Subscription, Balance
from django.utils import timezone


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'pay', 'available_courses']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс). задание 2.2"""
        # TODO
        user = request.user
        course = get_object_or_404(Course, id=pk)
        serializer = self.get_serializer(course)
        balance = Balance.objects.get(user=user)
        data = serializer.data

        if balance.amount < data['cost']:
            return Response(
                data={"error": "Недостаточно средств!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        balance.amount -= data['cost']
        balance.save()

        Subscription.objects.create(user_id=user.pk, course_id=data['id'])

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def available_courses(self, request):
        query_set = self.get_queryset()

        filtered_queryset = query_set.filter(
            start_date__gte=timezone.now()).filter(availability=True)

        not_subscribed = filtered_queryset.exclude(
            id__in=Subscription.objects.filter(
                user=request.user).values('course_id')
        )

        serializer = self.get_serializer(not_subscribed, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
