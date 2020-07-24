from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat.models import Dialogue, Message
from chat.serializers import DialogueSerializer, MessageSerializer, DialoguePostSerializer, MessagePostSerializer


class DialoguesView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        messages = Message.objects.filter(Q(sender_id=request.user.id) | Q(recipient_id=request.user.id)).order_by('-timestamp')

        dialogue_ids = []
        msgs = []

        for message in messages:
            if not message.dialogue.id in dialogue_ids:
                msgs.append(message)
                dialogue_ids.append(message.dialogue.id)

        serializer = MessageSerializer(msgs, many=True)

        return Response({'info': serializer.data})
    
    def post(self, request):
        serializer = DialoguePostSerializer(data=request.data)

        if serializer.is_valid():
            dialogue = serializer.save(request.user.id)
            return Response({'status': 'ok', 'created_dialogue': dialogue.id})
        
        return Response({'errors': serializer.errors})


class UnreadMessagesView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        messages = Message.objects.filter(recipient_id=request.user.id, \
            read=False)
        
        serializer = MessageSerializer(messages, many=True)

        return Response({'info': serializer.data})


class DialogueView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = MessagePostSerializer(data=request.data)

        if serializer.is_valid():
            message = serializer.save(request.user.id)
            return Response({'status': 'ok', 'sent_message': message.id})

        return Response({'errors': serializer.errors})

    
    def get(self, request):
        dialogue = Dialogue.objects.get(pk=request.query_params['dialogue'])

        if request.user.id != dialogue.buyer.id and \
            request.user.id != dialogue.seller.id:
            return HttpResponseForbidden('Access restricted.')

        Message.objects.filter(dialogue=dialogue, recipient_id=request.user.id,
                             read=False).update(read=True)
        messages = Message.objects.filter(dialogue=dialogue).order_by('timestamp')
        

        serializer = MessageSerializer(messages, many=True)

        return Response({'info': serializer.data})