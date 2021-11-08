from django.shortcuts import render
from django.test.testcases import SerializeMixin
from rest_framework import viewsets, generics, mixins, status
from rest_framework.response import Response
from .models import Board, Comment
from .serializers import BoardSerializer, BoardListSerializer, CommentSerializer
from .paginations import BoardPageNumberPagination
# Create your views here.

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.prefetch_related("comments")
    serializer_class = BoardSerializer
    pagination_class = BoardPageNumberPagination

    def _check_password(self, request, pk):
        board = Board.objects.filter(id=pk).first()
        if not board:
            return True
        password = request.META.get('HTTP_PASSWORD')
        if board.check_password(password):
            return False
        return True

    def list(self, request):
        boards = Board.objects.prefetch_related("comments").order_by('created_at')
        serializer = BoardListSerializer(boards, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
        
    def update(self, request, pk):
        if self._check_password(request, pk):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, pk)

    def partial_update(self, request, pk):
        if self._check_password(request, pk):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        board = self.queryset.get(id=pk)
        serializer = self.serializer_class(board,data= request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        if self._check_password(request, pk):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, pk)

class CommentCreateView(generics.CreateAPIView):
    queryest = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def _check_password(self, request, pk):
        board = Comment.objects.get(id=pk)
        password = request.META.get('HTTP_PASSWORD')
        if board.check_password(password):
            return False
        return True

    def update(self, request, pk):
        if self._check_password(request, pk):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, pk)

    def partial_update(self, request, pk):
        if self._check_password(request, pk):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(self.queryset.get(id=pk), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        if self._check_password(request, pk):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, pk)

    