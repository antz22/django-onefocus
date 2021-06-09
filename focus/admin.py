from django.contrib import admin

from .models import User, Task, Goal, Quote, Category

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Goal)
admin.site.register(Quote)
admin.site.register(Category)
