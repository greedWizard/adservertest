from rest_framework import serializers


def DataValidator(data, necessary_fields):
    for field in necessary_fields.all():
        if not field.name in data.keys():
            raise serializers.ValidationError('Не все необходимые поля в "data"')