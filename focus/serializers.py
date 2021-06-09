from rest_framework import serializers

from .models import User, Task, Goal, Quote, Category


class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category', read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "content",
            "category_name",
            "priority",
            "completed",
            "time"
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "category",
        )


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            "id",
            "goal",
            "progress",
            "progressLimit",
        )


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = (
            "id",
            "author",
            "content",
        )
