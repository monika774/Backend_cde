from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import BookListView, AdminBookCreateView, AdminBookRetrieveView, AdminBookUpdateView, AdminBookDeleteView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView

""" list of all APIS for CRUD Operations Admin and Normal User """

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/create/", AdminBookCreateView.as_view(), name="admin-create-book"),
    path("books/<int:pk>/", AdminBookRetrieveView.as_view(), name="admin-retrieve"),
    path("books/<int:pk>/update/", AdminBookUpdateView.as_view(), name="admin-update-book"),
    path("books/<int:pk>/delete/", AdminBookDeleteView.as_view(), name="admin-delete-book"),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
