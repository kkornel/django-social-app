import logging

from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

from .serializers import ProfileSerializer

logger = logging.getLogger(__name__)


class ProfileDetailAPiView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        try:
            profile = User.objects.get(
                username=self.kwargs['username']).profile
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
