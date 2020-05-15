from rest_framework import serializers

from coreapp.models import Tag,Ingredient,Recipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tag
        fields=('id','name')
        read_only_fields=('id',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model=Ingredient
        fields=('id','name')
        read_only_fields=('id',)

class RecipeSerializer(serializers.ModelSerializer):
    ingredients=serializers.PrimaryKeyRelatedField(
        many=True,queryset=Ingredient.objects.all
    )

    class Meta:
        model=Recipe
        fields=('id','title','ingredients','tags','price','time_minutes','link')
        read_only_fields=('id',)
