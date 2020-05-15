from rest_framework import viewsets,mixins
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from coreapp.models import Tag
from recipe import serializers

class TagViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
    authentication_classes=(TokenAuthentication)
    permission_classes=(IsAuthenticated,)
    queryset=Tag.objects.all()
    serializer_class=serializers.TagSerializer

    


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).orderby("-name")

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)