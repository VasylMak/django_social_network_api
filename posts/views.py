from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render
from django.views import View, generic

from .forms import RegisterForm
from .models import Post


def user_register(request):
    template = 'posts/register.html'
   
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username_form = form.cleaned_data['username']
            email_form = form.cleaned_data['email']
            password_form = form.cleaned_data['password']
            password_repeat_form = form.cleaned_data['password_repeat']
            if User.objects.filter(username=username_form).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=email_form).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif password_form != password_repeat_form:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()

                login(request, user)
               
                return HttpResponseRedirect(reverse_lazy('index'))
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            post.dislikes.remove(request.user)
        
        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            post.likes.add(request.user)
        
        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if is_like:
            post.likes.remove(request.user)
        
        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if not is_dislike:
            post.dislikes.add(request.user)
        
        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class UserListView(generic.ListView):
    model = User
    paginate_by = 20