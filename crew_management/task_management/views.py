# views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.utils import timezone

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10  # Adjust this value based on your preference

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).order_by('-due_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_view'] = 'tasks'
        context['pending_tasks'] = self.get_queryset().filter(status='pending').count()
        context['in_progress_tasks'] = self.get_queryset().filter(status='in_progress').count()
        context['completed_tasks'] = self.get_queryset().filter(status='completed').count()
        return context
    
    # views.py
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Task, TaskComment
from .forms import TaskCommentForm

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        return get_object_or_404(Task, id=self.kwargs['pk'], assigned_to=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_view'] = 'tasks'
        context['comment_form'] = TaskCommentForm()
        context['comments'] = self.object.comments.order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'update_status' in request.POST:
            new_status = request.POST.get('status')
            if new_status in dict(Task.STATUS_CHOICES):
                self.object.status = new_status
                self.object.save()
                messages.success(request, f"Task status updated to {self.object.get_status_display()}")
            else:
                messages.error(request, "Invalid status")
        elif 'add_comment' in request.POST:
            form = TaskCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.task = self.object
                comment.user = request.user
                comment.save()
                messages.success(request, "Comment added successfully")
            else:
                messages.error(request, "Error adding comment")
        return redirect(reverse('task_detail', kwargs={'pk': self.object.pk}))