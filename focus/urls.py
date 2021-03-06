from django.urls import path, include

from focus import views

urlpatterns = [
    path('create-task/', views.createTask),
    path('create-goal/', views.createGoal),
    path('delete-task/', views.deleteTask),
    path('delete-goal/', views.deleteGoal),
    path('app-register/', views.appRegister),
    path('app-login/', views.appLogin),
    path('tasks/', views.TasksList.as_view()),
    path('goals/', views.GoalsList.as_view()),
    path('categories/', views.CategoriesList.as_view()),
    path('quotes/', views.QuotesList.as_view()),
]
