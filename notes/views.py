from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note
from .forms import NoteForm

# Custom Login Required Mixin
class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, "You must be logged in to access this page.")
        return redirect('login')

# User Signup View - Public Access
class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully. You can now log in.")
        user = form.save()
        login(self.request, user)
        return redirect('note_list')  

# Login and Logout Views - Public Access
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Login successful!")
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "You have logged out successfully.")
        return super().dispatch(request, *args, **kwargs)

# Notes List with Pagination - Protected Access
class NoteListView(CustomLoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

# Note Detail View - Protected Access
class NoteDetailView(CustomLoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'

# Note Create View - Protected Access
class NoteCreateView(CustomLoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Note created successfully!")
        return super().form_valid(form)

# Note Update View - Protected Access
class NoteUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        messages.success(self.request, "Note updated successfully!")
        return super().form_valid(form)

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

# Note Delete View - Protected Access
class NoteDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Note deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
