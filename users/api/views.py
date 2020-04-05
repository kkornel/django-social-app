import logging

from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Profile, User

from .serializers import ProfileSerializer, UserSerializer

logger = logging.getLogger(__name__)


class UserListApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = (AllowAny, )

    # def list(self, request):
    #     """
    #     If we want 'status' in Response,
    #     otherwise leave it commented.
    #     """
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = UserSerializer(queryset, many=True)
    #     data = {'status': 'success', 'data': serializer.data}
    #     return Response(data)


class UserDetailAPiView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            # data = {'status': 'error', 'data': 'User not found.'}
            # return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
        # data = {'status': 'success', 'data': serializer.data}
        # return Response(data)


class ProfileListAPiView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    permission_classes = (AllowAny, )

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = ProfileSerializer(queryset, many=True)
    #     data = {'status': 'success', 'data': serializer.data}
    #     return Response(data)


class ProfileDetailAPiView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        try:
            profile = User.objects.get(
                username=self.kwargs['username']).profile
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            # data = {'status': 'error', 'data': 'Profile not found.'}
            # return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
        # data = {'status': 'success', 'data': serializer.data}
        # return Response(data)
