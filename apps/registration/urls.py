from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view, register_view

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset/form.html"
        ),
        name="password_reset"
    ),
    path("password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset/done.html"
        ),
        name="password_reset_done"
    ),
    path("reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset/confirm.html"
        ),
        name="password_reset_confirm"
    ),
    path("reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset/complete.html"
        ),
        name="password_reset_complete"
    ),
]
