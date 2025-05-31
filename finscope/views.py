from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@login_required
def task_assign_multiple(request):
    if request.method == "POST":
        selected_tasks = request.POST.getlist('selected_tasks')
        for task_id in selected_tasks:
            try:
                task = Task.objects.get(id=task_id)
                task.task_participants.add(request.user)
            except Task.DoesNotExist:
                continue
        return redirect('task_list')
    return redirect('task_list')


@login_required
def task_unassign_multiple(request):
    if request.method == "POST":
        unselected_tasks = request.POST.getlist('unselected_tasks')
        for task_id in unselected_tasks:
            try:
                task = Task.objects.get(id=task_id)
                task.task_participants.remove(request.user)
            except Task.DoesNotExist:
                continue
        return redirect('task_list')
    return redirect('task_list')


@login_required
def task_list(request):
    tasks = Task.objects.filter(is_active=True).exclude(task_participants=request.user)
    user_tasks = request.user.tasks.all() 
    context = {
        'tasks': tasks,
        'user_tasks': user_tasks,
    }
    return render(request, 'finscope/task_list.html', context)