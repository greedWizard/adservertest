from rest_framework import serializers

from users.serializers import UserSerializer
from chat.models import Dialogue, Message
from board.models import Ad
from board.serializers import AdSerializer, SubAdSerializer


class DialogueSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    buyer = UserSerializer()
    ad = SubAdSerializer()

    class Meta:
        model = Dialogue
        fields = ('id', 'ad', 'seller', 'buyer')


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    recipient = UserSerializer()
    dialogue = DialogueSerializer()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'read', 'text', 'timestamp', 'dialogue')


class DialoguePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialogue
        fields = ('ad', )

    def save(self, buyer_id):
        ad = self.validated_data['ad']
        seller_id = ad.author.id

        dialogue = Dialogue(ad=ad, seller_id=seller_id, buyer_id=buyer_id)
        dialogue.save()

        txt = 'Здравствуйте, меня заинтересовал данный товар.'
        msg = Message(dialogue=dialogue, sender_id=buyer_id, recipient_id=seller_id, text=txt)
        
        msg.save()

        return dialogue


class MessagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('dialogue', 'recipient', 'text')

    def save(self, sender_id):
        if not self.validated_data['dialogue'].ad:
            raise serializers.ValidationError('Ad is empty')

        message = Message(dialogue=self.validated_data['dialogue'], \
                            sender_id=sender_id, \
                            recipient=self.validated_data['recipient'], \
                            text=self.validated_data['text']
                        )

        message.save()

        return message
