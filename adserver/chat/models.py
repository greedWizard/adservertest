from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from board.models import Ad


class Dialogue(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.SET_NULL, related_name='dialogues',  null=True)
    buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='buyer_dialogues')
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='seller_dialogues')

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError('Dialogue should be immutable')
        if Dialogue.objects.filter(ad_id=self.ad.id) and \
            Dialogue.objects.filter(seller_id=self.seller.id) and \
            Dialogue.objects.filter(buyer_id=self.buyer.id):
            raise ValidationError('Dialogue already exists')
        if self.buyer.id == self.seller.id:
            raise ValidationError('Self messaging is not allowed')

        self.seller = self.ad.author
        
        super(Dialogue, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.ad.title}: {self.seller} -> {self.buyer}'


class Message(models.Model):
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender_messages')
    recipient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='recipient_messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if (    
                self.sender.id != self.dialogue.seller.id and \
                self.sender.id != self.dialogue.buyer.id) or \
                (self.recipient.id != self.dialogue.seller.id and \
                self.recipient.id != self.dialogue.buyer.id
            ):
            raise models.exceptions.ValidationError('Invalid users. Recipient/sender should be either buyer or sender.')
        
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.sender.username} -> {self.recipient.username}: "{self.text[:50]}" {self.timestamp}'