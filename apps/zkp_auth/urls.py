from django.urls import path

from . import views

app_name = "zkp_auth"

urlpatterns = [
    path("register/", views.ZKPRegisterView.as_view(), name="zkp_register"),
    path("challenge/", views.ZKPChallengeView.as_view(), name="zkp_challenge"),
    path("verify/", views.ZKPVerifyView.as_view(), name="zkp_verify"),
    path("login-ui/", views.zkp_login_page, name="zkp_login_page"),
    path("tokens/generate/", views.GitTokenGenerateView.as_view(), name="git_token_generate"),
    path("tokens/validate/", views.GitTokenValidateView.as_view(), name="git_token_validate"),
]
