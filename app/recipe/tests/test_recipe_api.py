from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from coreapp.models import Recipe,Tag,Ingredient

from recipe.serializers import RecipeSerializer,RecipeDetailSerializer

RECIPE_URL=reverse('recipe:recipe-list')

def detail_URL(recipe_id):
    return reverse('recipe:recipe-detail',args=[recipe_id])

def sample_ingredients(user,name='Cinnamon'):
    return Ingredient.objects.create(user=user,name=name)

def sample_tags(user,name='Main_Course'):
    return Tag.objects.create(user=user,name=name)

def sample_recipe(user,**params):
    defaults={
        'title':'Sample Recipe',
        'time_minutes':10,
        'price':14.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user,**defaults)



class PublicRecipeApiTests(TestCase):
    def setUp(self):
        self.client=APIClient()

    def test_login_required(self):
        res=self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    def setUp(self):
        self.client=APIClient()
        self.user=get_user_model().objects.create_user(
            'arialkk@gmail.com','lebronjames'

        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        res=self.client.get(RECIPE_URL)

        recipes=Recipe.objects.all().order_by("-id")
        serializer=RecipeSerializer(recipes,many=True)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)


    def test_recipe_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'password123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        recipe=sample_recipe(user=self.user)
        recipe.tags.add(sample_tags(user=self.user))
        recipe.ingredients.add(sample_ingredients(user=self.user))

        url=detail_URL(recipe.id)

        res=self.client.get(url)
        serializer=RecipeDetailSerializer(recipe)
        self.assertEqual(res.data,serializer.data)

    def test_create_basic_recipe(self):
        payload={
        'title':'Chocolate Cake','time_minutes':30,'price':5
        }
        res=self.client.post(RECIPE_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        recipe=Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key],getattr(recipe,key))

    def test_create_recipe_with_tags(self):
        tag1=sample_tags(user=self.user,name='Vegan')
        tag2=sample_tags(user=self.user,name='Dessert')

        payload={
        'title':'Avocado cheesecake',
        'tags':[tag1.id,tag2.id],
        'time_minutes':60,
        'price':100.00
        }
        res=self.client.post(RECIPE_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        recipe=Recipe.objects.get(id=res.data['id'])
        tags=recipe.tags.all()
        self.assertIn(tag1,tags)
        self.assertIn(tag2,tags)

    def test_create_recipe_with_ingredients(self):
        ingredient1=sample_ingredients(user=self.user,name='Prawn')
        ingredient2=sample_ingredients(user=self.user,name='Chicken')

        payload={
        'title':'Avocado cheesecake',
        'ingredients':[ingredient1.id,ingredient2.id],
        'time_minutes':60,
        'price':100.00
        }
        res=self.client.post(RECIPE_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        recipe=Recipe.objects.get(id=res.data['id'])
        ingredients=recipe.ingredients.all()
        self.assertIn(ingredient1,ingredients)
        self.assertIn(ingredient2,ingredients)

    def test_partial_update_recipe(self):
        """Test updating a recipe with patch"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='Curry')

        payload = {'title': 'Chicken tikka', 'tags': [new_tag.id]}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """Test updating a recipe with put"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        payload = {
            'title': 'Spaghetti carbonara',
            'time_minutes': 25,
            'price': 5.00
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)
