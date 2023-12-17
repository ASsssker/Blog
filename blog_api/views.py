from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, permissions
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from blog.models import Post
from blog_api.sericalizers import PostSerializer
from blog_api.permissions import IsAuthorOrReadOnly

# Create your views here.

class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['body', 'author__username']
    #ordring_fields = ['author_id', 'publish']
    ordering_fields = '__all__'
    ordering = ['id']
    

class UserPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        user = self.kwargs['username']
        return Post.objects.filter(author=user)
    

    

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


"""
class PostList(APIView):
    def get(self, request, format=None):
        transformers = Post.objects.all()
        serializer = PostSerializer(transformers, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        transformer = self.get_object(pk)
        serializer = PostSerializer(transformer)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        transformer = self.get_object(pk=pk)
        serializer = PostSerializer(transformer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        transformer = self.get_object(pk=pk)
        serializer = PostSerializer(transformer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        transformer = self.get_object(pk)
        transformer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""