from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, exceptions


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class RequestEMtoODSerializer(ModelSerializer):
    class Meta:
        model = RequestEMtoOD
        exclude = ('user',)


class RequestEMtoOESerializer(ModelSerializer):
    class Meta:
        model = RequestEMtoOE
        exclude = ('user',)


class RequestOEtoODSerializer(ModelSerializer):
    class Meta:
        model = RequestOEtoOD
        exclude = ('user',)

class LoginSerilizer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField()

    def validate(self, data):

        username = data.get("username", "")

        password = data.get("password", "")

        if username and password:

            user = authenticate(username=username, password=password)

            if user:

                if user.is_active:

                    data["user"] = user

                else:

                    msg = "کاربر غیرفعال می باشد"

                    raise exceptions.ValidationError(msg)

            else:

                msg = "نام کاربری یا گذرواژه اشتباه است"

                raise exceptions.ValidationError(msg)

        else:

            msg = "نام کاربری و کلمه عبور اجباری می باشد"

            raise exceptions.ValidationError(msg)

        return data

class Answerserializer(serializers.Serializer):
    ANSWER = [
        ('true' , 'موافقت با این درخواست'),
        ('false' , 'رد این  درخواست'),
    ]

    answer = serializers.ChoiceField(ANSWER)


class Manageserializer(serializers.Serializer):
    STATUS = [
        ('od', 'مدیر سازمان'),  # مدیر سازمان
        ('oe', 'کارمند سازمان'),  # کارمند سازمان
        ('em', 'کارمند'),  # کارمند
    ]

    profile = serializers.ModelField(model_field=Profile)
    status = serializers.ChoiceField(STATUS)

# class PostUpdateSerializer(ModelSerializer):
#     class Meta:
#         model = Posts
#         fields = '__all__'
#
#
# class PostCreateSerializer(ModelSerializer):
#     class Meta:
#         model = Posts
#         # fields = '__all__'
#         exclude = ('owner',)
#
#
# class PostDeleteUpdateSerializer(ModelSerializer):
#     class Meta:
#         model = Posts
#         fields = '__all__'
#
#
# class LoginSerilizer(serializers.Serializer):
#     username = serializers.CharField()
#
#     password = serializers.CharField()
#
#     def validate(self, data):
#
#         username = data.get("username", "")
#
#         password = data.get("password", "")
#
#         if username and password:
#
#             user = authenticate(username=username, password=password)
#
#             if user:
#
#                 if user.is_active:
#
#                     data["user"] = user
#
#                 else:
#
#                     msg = "کاربر غیرفعال می باشد"
#
#                     raise exceptions.ValidationError(msg)
#
#             else:
#
#                 msg = "نام کاربری یا گذرواژه اشتباه است"
#
#                 raise exceptions.ValidationError(msg)
#
#         else:
#
#             msg = "نام کاربری و کلمه عبور اجباری می باشد"
#
#             raise exceptions.ValidationError(msg)
#
#         return data
#
#
# class Userserializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
