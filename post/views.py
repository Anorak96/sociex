from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
import json
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core import serializers
from itertools import chain
from .forms import ImageForm, PostForm, CommentForm
from .models import Post, Comment, Image
from user.models import User

def post_json(request):
    qs = Post.objects.all()
    data = serializers.serialize('json', qs)
    return JsonResponse({'data': data})

def posts(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_spin.html', context)

class PostListView(LoginRequiredMixin, generic.ListView):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = "post/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ = self.kwargs.get("pk")
        user = User.objects.get(pk=self.request.user.pk) # get object of logged in user
        following = [prof for prof in user.following.all()] # profile that logged in user is folowing
        posts = []
        qs = None
        #=== following posts===
        for us in following:
            u_post = us.user_post.all()
            posts.append(u_post)
        my_post = self.request.user.user_post.all()
        posts.append(my_post)
        #=== sort and chain post query===
        if len(posts)>0:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created_at)
        context['posts'] = qs
        
        # paginator = Paginator(qs, 1)
        # page_number = self.request.GET.get('page')
        # context['posts'] = paginator.get_page(page_number)
        
        context['user_self'] = User.objects.get(pk=self.request.user.pk)
        user = self.request.user.pk
        context['users'] = User.objects.get_user_to_follow(pk=user)
        return context 

class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ = self.kwargs.get("pk")
        context['post'] = Post.objects.get(pk=pk_)
        post = Post.objects.get(pk=pk_)
        context['comments'] = Comment.objects.filter(post=post)
        context['form'] = CommentForm()
        return context

class LikeView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            likes_no = post.likes_no()
        else:
            post.likes.add(request.user)
            likes_no = post.likes_no()
        data = {
            'likes_no': likes_no,
            'post_id': id,
        }
        return JsonResponse(data, safe=False)

class PostCreate(LoginRequiredMixin, generic.View):
    template_name = 'post/create.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        form = PostForm()
        return render(request, self.template_name, context={'form':form })

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        images = request.FILES.getlist("images")
        user = User.objects.get(pk=request.user.pk)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            
            for i in images:
                image = Image.objects.create(post=instance, image=i)
                image.save()

            return redirect(user.get_absolute_url())
        else:
            print(form.errors)
        
        imageform = ImageForm()
        context = {'form': form, 'imageform': imageform}
        return render(request, self.template_name, context)

class CommentCreate(LoginRequiredMixin, generic.View):
    template_name = 'post/detail.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
        
    def get(self, request):
        form = CommentForm()
        return render(request, self.template_name, context={'form':form })

    def post(self, request):
        form = CommentForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.post = Post.objects.get(id=request.POST.get('post_comment'))
            instance.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
        
        context = {'form': form}
        return render(request, self.template_name, context)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'post/delete.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        return reverse('post:posts')

    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk_)
        return post.user == self.request.user

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'post/delete.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse('post:detail', kwargs={"pk": pk})

    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk_)
        return post.user == self.request.user

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post    
    form_class = PostForm
    template_name = 'post/update.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse('post:detail', kwargs={"pk": pk})

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        images = self.request.FILES.getlist("images")
        if form.instance.user == user:
            for i in images:
                image = Image.objects.create(post=form.instance, image=i)
                image.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'Post not yours')
            return super().form_invalid(form)
    
    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk_)
        return post.user == self.request.user

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment    
    form_class = CommentForm
    template_name = 'post/update.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse('post:detail', kwargs={"pk": pk})

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        if form.instance.user == user:
            return super().form_valid(form)
        else:
            form.add_error(None, 'Comment is  not yours')
            return super().form_invalid(form)
    
    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk_)
        comment = Comment.objects.filter(post=post)
        return comment.user == self.request.user