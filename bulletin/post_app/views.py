from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView, View, TemplateView
from .models import Post, Reply, Profile
from .forms import PostForm, ReplyForm
from django.contrib.auth.models import User
from .sample_app.filters import ReplyFilter
from .permissions import AuthorPermissionMixin


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def form_valid(self, form, **kwargs):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect('/posts/list')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replyform'] = ReplyForm
        context['postreplies'] = Reply.objects.filter(post=self.get_object().id)
        return context


class PostDelete(AuthorPermissionMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts')
    template_name = 'post_delete.html'


class PostUpdate(AuthorPermissionMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'


class UserPost(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=self.request.user)
        return context


class ReplyCreate(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'post.html'

    def form_valid(self, form, **kwargs):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.post_id = self.request.get_object().id
        instance.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ReplyForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = self.request.user
                instance.post_id = self.kwargs.get('pk')
                instance.save()
                return redirect('/posts/list')


class UserReplies(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'userreplies.html'
    context_object_name = 'userreplies'

    def get_queryset(self):
        queryset = super().get_queryset().filter(post__user=self.request.user)
        self.filterset = ReplyFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def change_status(request):
    reply_id = request.POST['id']
    reply = Reply.objects.get(id=reply_id)
    if reply.status:
        reply.status = False
    else:
        reply.status = True
    reply.save()

    return redirect('/posts/userreplies')


class ReplyDelete(AuthorPermissionMixin, DeleteView):
    model = Reply
    success_url = '/posts/userreplies'


@login_required
def subscribe(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile.subscribe = 1
    profile.save()
    return redirect('/')




