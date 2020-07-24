from django.urls import path, include
from chat.views import DialoguesView, DialogueView, UnreadMessagesView

urlpatterns = [
    path('dialogues/', DialoguesView.as_view()),
    path('messages/', DialogueView.as_view()),
    path('messages/new/', UnreadMessagesView.as_view()),
]