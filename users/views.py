from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views.generic import CreateView, TemplateView
from .forms import LoginForm, SignUpForm


class Top(TemplateView):
    template_name = 'users/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('sake_log:index')


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'users/logout.html'


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "users/signup.html" 
    success_url = reverse_lazy('sake_log:index')

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        login(self.request, user) # 認証
        self.object = user 
        return HttpResponseRedirect(self.get_success_url()) # リダイレクト