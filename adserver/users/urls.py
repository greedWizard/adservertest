from django.urls import path, include
from .views import Users, AuthorizedUser, UserView, User, CreateUser, ProfileUpdateView, UpdateUserView

urlpatterns = [
    path('', Users.as_view()),
    path('profile/', AuthorizedUser.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),
    path('register/', CreateUser.as_view()),
    path('update/', UpdateUserView.as_view()),
    path('profile/<int:user_id>/', UserView.as_view()),
]