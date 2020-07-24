from rest_framework import serializers

from string import ascii_letters


def PhoneValidator(number):
    if len(number) < 11 or len(number) > 20: 
        raise serializers.ValidationError('Неправильный номер')
    if '+' in number: raise serializers.ValidationError('Неправильный номер')
    
    letters = ascii_letters

    for letter in letters:
        if letter in number:
            raise serializers.ValidationError('Неправильный номер')