from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user=User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class StudentSerializers(serializers.ModelSerializer):

    class Meta:
        model=Student
        # fields=['name','age']
        # exclude=['id',]
        fields="__all__"

    # always validate your logic here not views.py
    def validate(self, data):
        if data['age']<18:
            raise serializers.ValidationError({
                'error':"age cant't be less than 18"
            })
        if data['name']:
            for n in data['name']:
                if n.isdigit():
                    raise serializers.ValidationError({
                        'error':"name can't be numeric"
                    })
        return data
    

class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields="__all__"

class BookSerializers(serializers.ModelSerializer):
    category=CategorySerializers()
    class Meta:
        model=Book
        fields="__all__"