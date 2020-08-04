from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from chat.models import Message, Dialogue

from django.db import close_old_connections



class MessageConsumer(WebsocketConsumer):
    def connect(self):
        self.dialogue_id = self.scope['url_route']['kwargs']['dialogue_id']
        self.dialogue_group_name = 'dialogue_%s' % self.dialogue_id

        async_to_sync(self.channel_layer.group_add)(
            self.dialogue_group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.dialogue_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data = json.loads(text_data)
        message = text_data['message']
        recipient_id = text_data['recipient_id']
        sender_id = text_data['sender_id']
        dialogue_id = text_data['dialogue_id']

        Message(
            text=message,
            recipient_id=recipient_id,
            sender_id=sender_id,
            dialogue_id=dialogue_id,
        ).save()

        close_old_connections()

        async_to_sync(self.channel_layer.group_send)(
            self.dialogue_group_name,
            {
                'type': 'dialogue_message',
                'message': message,
                'sender_id': sender_id,
                'recipient_id': recipient_id,
            }
        )

    def dialogue_message(self, event):
        message = event['message']
        recipient_id = event['recipient_id']
        sender_id = event['sender_id']

        data = {
            'message': message,
            'recipient_id': recipient_id,
            'sender_id': sender_id,
        }

        self.send(text_data=json.dumps(data))


# class NewMessagesConsumer(WebsocketConsumer):
#     def connect(self):
#         self.user_name = self.scope['url_route']['kwargs']['user_name']
#         self.user_group_name = f'new_messages_{self.user_name}'

#         async_to_sync(self.channel_layer_group_add)(
#             self.user_group_name,
#             self.channel_name,
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.user_group_name,
#             self.channel_name,
#         )

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)

#     def chat_message(self, event):
#         pass
