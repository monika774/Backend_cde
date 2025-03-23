import jwt
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Book
from .serializers import BookSerializer, MyTokenObtainPairSerializer




class MyTokenObtainPairView(TokenObtainPairView):
    "serializers for TokenObtainPair View"
    serializer_class = MyTokenObtainPairSerializer  



class DecodeTokenView(APIView):
    """ Code for decode Token """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]

        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token['user_id']
            is_admin = decoded_token['is_admin']

            return Response({
                'user_id': user_id,
                'is_admin': is_admin
            })

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)



class BookListView(generics.ListAPIView):
    """Logic for list view book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  



class AdminBookCreateView(generics.CreateAPIView):
    """Logic for Admin create book """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(added_by=request.user)
                return Response(
                    {"message": "Book created successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response({"error": "Database Integrity Error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class AdminBookRetrieveView(generics.RetrieveAPIView):
    """Logic Retrieve book by id """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser] 

    def get_object(self):
        return get_object_or_404(Book, pk=self.kwargs["pk"]) 



class AdminBookUpdateView(generics.UpdateAPIView):
    """Admin book update code """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]  

    def update(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs["pk"])  
        serializer = self.get_serializer(book, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {"message": "Book updated successfully", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            except IntegrityError:
                return Response({"error": "Database Integrity Error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class AdminBookDeleteView(generics.DestroyAPIView):
    """Admin delete book code """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]  

    def destroy(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs["pk"])
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
