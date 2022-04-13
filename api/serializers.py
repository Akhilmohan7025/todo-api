from rest_framework.serializers import ModelSerializer
from api.models import Todos
from django.contrib.auth.models import User
from rest_framework import serializers


class Todoserilizers(ModelSerializer):
    class Meta:
        model = Todos
        fields = ['id', 'task_name', 'user', 'completed_success']
        read_only_field = ['id']
        depth = 1


class Usercreationserilizer(ModelSerializer):
    class Meta():
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validation_data):
        return User.objects.create_user(**validation_data)


class Loginserilizer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

