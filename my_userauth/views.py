from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm.. this was default implementation before adding email field
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, ProfileCreateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)
from .models import Profile
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(ListView):
    model = Profile
    template_name = 'my_userauth/profile_list.html'
    # default it is object_list so u can override to profile
    context_object_name = 'profile'
    ordering = ['-date_created']


class PostDetailView(DetailView):
    model = Profile
    #template_name = 'my_userauth/profile_list.html'
    #queryset = Profile.objects.all()
    template_name = 'my_userauth/profile_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        #id_ = 2
        print(id_)
        return get_object_or_404(Profile, id=id_)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = 'my_userauth/profile_form.html'
   # fields = ['user', 'image'],, i can define template name or crete model_form.html

    def form_valid(self, form):
        print(form.cleaned_data)
        form.instance.user = self.request.user
        return super().form_valid(form)


def home(request):
    #name = 'hello'
   # args = {'msg': 'arti'}
    # return(HttpResponse("Home page"))
    return render(request, 'my_userauth/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account has been created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()  # get request

    return render(request, 'my_userauth/login.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Your Account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form

    }
    return render(request, 'my_userauth/profile.html', context)
