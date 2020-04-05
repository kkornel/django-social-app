import logging

from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Comment, Like, Post

from .serializers import CommentSerializer, LikeSerializer, PostSerializer

logger = logging.getLogger(__name__)
#
# Different ways:
#
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

    # def list(self, request):
    #     """
    #     If we want 'status' in Response,
    #     otherwise leave it commented.
    #     """
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = PostSerializer(queryset, many=True)
    #     data = {'status': 'success', 'data': serializer.data}
    #     return Response(data)


class PostDetailApiView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(pk=self.kwargs['id'])
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            # data = {'status': 'error', 'data': 'Post not found.'}
            # return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)
        # data = {'status': 'success', 'data': serializer.data}
        # return Response(data)


class CommentListApiView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    permission_classes = (AllowAny, )

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = CommentSerializer(queryset, many=True)
    #     data = {'status': 'success', 'data': serializer.data}
    #     return Response(data)


class CommentDetailApiView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=self.kwargs['id'])
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            # data = {'status': 'error', 'data': 'Comment not found.'}
            # return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
        # data = {'status': 'success', 'data': serializer.data}
        # return Response(data)


class LikeListApiView(generics.ListAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    permission_classes = (AllowAny, )

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = LikeSerializer(queryset, many=True)
    #     data = {'status': 'success', 'data': serializer.data}
    #     return Response(data)


class LikeDetailApiView(generics.RetrieveAPIView):
    serializer_class = LikeSerializer
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        try:
            like = Like.objects.get(pk=self.kwargs['id'])
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            # data = {'status': 'error', 'data': 'Like not found.'}
            # return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = LikeSerializer(like)
        return Response(serializer.data)
        # data = {'status': 'success', 'data': serializer.data}
        # return Response(data)
