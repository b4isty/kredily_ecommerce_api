from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from accounts.serializers import SignupSerializer


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    queryset = get_user_model().objects.all()
