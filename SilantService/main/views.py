from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .rest_api import LoginRequestSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request: Request):
    serializer = LoginRequestSerializer(data=request.data)
    if serializer.is_valid():
        authenticated_user = authenticate(**serializer.validated_data)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return Response({'username': authenticated_user.username})
        else:
            return Response({'error': 'Invalid credentials'}, status=403)
    else:
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def logout_api(request: Request):
    logout(request)
    return Response()


@api_view(['GET'])
@permission_classes([AllowAny])
def user_info(request: Request):
    if request.user.is_authenticated:
        result = {
            'logged': True,
            'username': request.user.username
        }
    else:
        result = {
            'logged': False,
        }
    return Response(result)
