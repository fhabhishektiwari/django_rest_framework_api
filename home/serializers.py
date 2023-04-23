from rest_framework import serializers
from .models import *

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