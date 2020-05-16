from rest_framework import viewsets,mixins
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from coreapp.models import Tag,Ingredient,Recipe
from recipe import serializers

class BaseRecipeAttrViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin):
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()


    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttrViewSet):
    queryset=Tag.objects.all()
    serializer_class=serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    queryset=Ingredient.objects.all()
    serializer_class=serializers.IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class=serializers.RecipeSerializer
    queryset=Recipe.objects.all()
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action== 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
