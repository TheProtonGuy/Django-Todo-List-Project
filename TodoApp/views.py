from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Todo
from django.contrib import messages

@login_required
def home(request):

    user = request.user

    if request.method == 'POST':
        task = request.POST.get('task')

        # create a new todo item
        new_task = Todo(
            user = user,
            content = task
        )
        new_task.save()

        messages.success(request, 'New task saved successfully!')
        return redirect('home')

    user_tasks = Todo.objects.filter(user=user).order_by('-timestamp')

    finished_tasks = user_tasks.filter(is_completed=True).count()
    unfinished_tasks = user_tasks.filter(is_completed=False).count()

    context = {
        'tasks': user_tasks,
        'finished_tasks': finished_tasks,
        'unfinished_tasks': unfinished_tasks
    }

    return render(request, 'homepage/index.html', context)

@login_required
def delete_task(request, task_id):

    try:
        task = Todo.objects.get(id=task_id)
        task.delete()

        messages.success(request, 'Task deleted successfully')
        return redirect('home')
    
    except Todo.DoesNotExist:
        messages.error(request, 'No task with that id exists in the database')
        return redirect('home')

@login_required
def update_task_status(request, task_id):

    try:
        task = Todo.objects.get(id=task_id)
        
        if task.is_completed:
            task.is_completed = False
        else:
            task.is_completed = True

        task.save()

        messages.success(request, 'Task updated successfully')
        return redirect('home')
    
    except Todo.DoesNotExist:
        messages.error(request, 'No task with that id exists in the database')
        return redirect('home')