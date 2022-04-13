from django.shortcuts import render
from rest_framework.views import APIView
from api.models import Todos
from api.serializers import Todoserilizers, Usercreationserilizer, User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins, viewsets
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from api.serializers import Loginserilizer
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token


# Create your views here.
class Todosview(APIView):
    def get(self, request, *args, **kwargs):
        todo = Todos.objects.all()
        serializers = Todoserilizers(todo, many=True)
        return Response(serializers.data)

    def post(self, request, *args, **kwargs):
        serializers = Todoserilizers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class Todosdetails(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        todo = Todos.objects.get(id=id)
        serializer = Todoserilizers(todo)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        todos = Todos.objects.get(id=id)
        serializer = Todoserilizers(instance=todos, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        id = kwargs.get("id")
        todo = Todos.objects.get(id=id)
        todo.delete()
        return Response({"message:deleted"}, status=status.HTTP_200_OK)


class todosmixinview(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    queryset = Todos.objects.all()
    serializer_class = Todoserilizers
    model = Todos

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class todomixinDetail(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Todos.objects.all()
    serializer_class = Todoserilizers
    model = Todos
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return (self.update(request, *args, **kwargs))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'sanam poi'})

    def delete(self, request, *args, **kwargs):
        return (self.destroy(request, *args, **kwargs))


class usercreationview(generics.GenericAPIView,
                       mixins.CreateModelMixin):
    serializer_class = Usercreationserilizer
    queryset = User.objects.all()
    model = User

    def get(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Todosviewsets(viewsets.ViewSet):
    model = Todos
    serializer_class = Todoserilizers

    def list(self, request):
        todo = Todos.objects.all()
        serializer = Todoserilizers(todo, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializers = Todoserilizers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        todo = Todos.objects.get(pk=pk)
        serializer = Todoserilizers(todo)
        return Response(serializer.data)

    def update(self, request, pk=None):
        todo = Todos.objects.get(id=pk)
        serializer = Todoserilizers(instance=todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destory(self, request, pk=None):
        todo = Todos.objects.get(id=pk)
        todo.delete()
        return Response({"message:delete"}, status=status.HTTP_201_CREATED)


class Todosmodelviewsets(viewsets.ModelViewSet):
    model = Todos
    queryset = Todos.objects.all()
    serializer_class = Todoserilizers
    # authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = Todoserilizers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Todos.objects.filter(user=request.user)
        serializer = Todoserilizers(queryset, many=True)
        return Response(serializer.data)


@action(methods=['GET', ], detail=False)
def completed_todos(self, request, *args, **kwargs):
    queryset = Todos.object.filter(completed_status=True, user=request.user)
    serializer = Todoserilizers(queryset, many=True)
    return Response(serializer.data)


@action(methods=['GET', ], detail=False)
def pending_todos(self, request, *args, **kwargs):
    queryset = Todos.object.filter(completed_status=False, user=request.user)
    serializer = Todoserilizers(queryset, many=True)
    return Response(serializer.data)


class loginviews(viewsets.ViewSet):
    model = User
    Serializer_class = Loginserilizer

    def create(self, request):
        serializer = self.Serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
