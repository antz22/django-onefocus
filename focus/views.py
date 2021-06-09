import json
import stripe
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import User, Task, Goal, Quote, Category
from .serializers import GoalSerializer, TaskSerializer, QuoteSerializer, CategorySerializer


class TasksList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def get_queryset(self, request, format=None):
        category = self.request.query_params.get('category')
        tasks = Task.objects.filter(user=request.user, category=category)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class GoalsList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        goals = Goal.objects.filter(user=request.user)
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)


class CategoriesList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class QuotesList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        quotes = Quote.objects.all()
        quote = random.choice(quotes)
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def createTask(request):

    task_data = request.data

    if 'content' in task_data:

        content = task_data['content']
        time = task_data['time']
        completed = task_data['completed']
        category = task_data['category']
        priority = task_data['priority']


        if Category.objects.filter(category=category, user=request.user).exists():
            task_category = Category.objects.get(category=category, user=request.user)
        else:
            task_category = Category.objects.create(category=category, user=request.user)

        task = Task.objects.create(user=request.user, content=content, category=task_category, priority=priority, time=time, completed=completed)
        task.save()

        return Response(status=status.HTTP_201_CREATED)

    else:

        task_id = task_data['id']
        completed = task_data['completed']
        task = Task.objects.get(user=request.user, id=task_id)
        task.completed = completed
        task.save()

        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deleteTask(request):

    task_data = request.data
    id = task_data['id']
    task = Task.objects.get(user=request.user, id=id)
    task.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def createGoal(request):

    goal_data = request.data

    if 'goal' in goal_data:

        goal = goal_data['goal']
        progress = goal_data['progress']
        progressLimit = goal_data['progressLimit']

        goal = Goal.objects.create(user=request.user, progress=progress, progressLimit=progressLimit, goal=goal)
        goal.save()

        return Response(status=status.HTTP_201_CREATED)

    else:

        goal_id = goal_data['id']
        progress = goal_data['progress']
        goal = Goal.objects.get(user=request.user, id=goal_id)
        goal.progress = progress
        goal.save()

        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deleteGoal(request):

    goal_data = request.data
    id = goal_data['id']
    goal = Goal.objects.get(user=request.user, id=id)
    goal.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def createCategory(request):

    data = request.data

    name = data['category']

    category = Category.objects.create(user=request.user, category=name)
    category.save()

    return Response(status=status.HTTP_201_CREATED)


def appRegister(request):

    username = request.POST["username"]
    password = request.POST["password"]

    try:
        user = User.objects.create_user(username, password)
        user.save()

    except IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_201_CREATED)


def appLogin(request):
    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)