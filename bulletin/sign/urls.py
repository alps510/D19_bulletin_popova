from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import usual_login_view, login_with_code_view, EnterCodeView

urlpatterns = [
    path('login/', usual_login_view,  name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('code/', login_with_code_view, name='codeview'),
    path('entercode/', EnterCodeView.as_view(), name='entercode'),
]