from django.urls import path
from .views import RegisterView

app_name = "accounts"


urlpatterns = [
    path('sign-up',RegisterView.as_view())
]
