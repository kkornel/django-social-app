import logging

from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Post

from .serializers import PostSerializer

logger = logging.getLogger(__name__)
# class PostListView(APIView):
#     permission_classes = (AllowAny, )

#     def get(self, request, *args, **kwargs):
#         queryset = Post.objects.all()
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data)

# class PostListView(mixins.ListModelMixin, generics.GenericAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()

#     permission_classes = (AllowAny, )

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


class PostListAPiView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    permission_classes = (AllowAny, )


class PostDetailApiView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['id'])
        serializer = PostSerializer(post)
        return Response(serializer.data)