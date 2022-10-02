from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from post.forms import PostForm
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .models import User
from django.http import JsonResponse
from post.models import Post, Image, Comment

class RegisterView(generic.View):
    template_name = 'user/register.html'

    def get(self, request):
        message = ''
        form = CreateUserForm()
        return render(request, self.template_name, context={'message': message, 'form':form })

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect(request.user.get_absolute_url())

        context = {'form':form,}
        return render(request, self.template_name, context)

class LoginView(generic.View):
    template_name = 'user/login.html'
    redirect_authenticated_user=True
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('post:posts')
            pass
        return render(request, self.template_name)
        
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
            return redirect('post:posts')
        else:
            messages.info(request, 'Username or Password Incorrect.')
        return render(request, self.template_name)

class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect('user:login')

class UserDetailView(FormMixin, generic.DetailView):
    model = User
    template_name = "user/profile.html"
    context_object_name = 'profiles'
    form_class = PostForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("user:profile", kwargs={"pk": pk})
    
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        pk_ = self.kwargs.get("pk")
        pk = User.objects.get(pk=pk_)
        context['posts'] = Post.objects.filter(user=pk)
        context['form'] = PostForm()
        user = self.request.user.pk
        context['photos'] = Image.objects.filter(post__user=pk).order_by('post')
        context['users'] = User.objects.get_user_to_follow(pk=user)
        
        users = User.objects.get_user_to_follow(pk=user)
        for user in users:
            other_follow = user.get_following()
            user_follow = self.request.user.get_following()
            friends = []
            for f1 in user_follow:
                for f2 in other_follow:
                    if f1 == f2:
                        mut_user = f1
                        friends.append(mut_user)
        return context

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
            messages.success(request, "Post Created")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(UserDetailView, self).form_valid(form)

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user/update.html"
    login_url = 'user:login'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("user:profile", kwargs={"pk": pk})

    def form_valid(self, form):
        if form.instance.pk == self.request.user.pk:
            form.instance.username = self.request.user.username
            return super().form_valid(form)
        else:
            form.add_error(None, 'Post not yours')
            return super().form_valid(form)

    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        user = User.objects.get(pk=pk_)
        return user == self.request.user

class FollowView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to' 

    def post(self, request, pk):
        my_profile = User.objects.get(pk=request.user.pk)
        # other profiles
        pk = request.POST.get('prof_pk')
        profile = get_object_or_404(User, pk=pk)

        if my_profile == profile:
            messages.info("You can't follow yourself")
        else:
            if profile in my_profile.following.all():
                my_profile.following.remove(profile)
                profile.follower.remove(my_profile)
            else:
                my_profile.following.add(profile)
                profile.follower.add(my_profile)
            return redirect(request.META.get('HTTP_REFERER'))

    # def post(self, request):
    #     return JsonResponse('it works', safe=False)