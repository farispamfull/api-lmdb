from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from .serializer import SignUpSerializer
from .utils import send_token_for_user


class SignUpApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, _ = User.objects.get_or_create(
            email=email, username=username,
            is_active=False
        )
        send_token_for_user(request, user)
        return Response({'email': email}, status=status.HTTP_200_OK)
   