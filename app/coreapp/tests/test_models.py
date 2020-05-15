from django.test import TestCase
from django.contrib.auth import get_user_model
from coreapp import models

def sample_user(email='test@london.com',password='yomom'):
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):


    def test_create_user_with_email(self):
        email='neelkk@gmail.com'
        password='arc123'
        user=get_user_model().objects.create_user(
        email=email,
        password=password

        )

        self.assertEqual(user.email,email)
        self.assertEqual(user.check_password(password),True)


    def test_new_user_normalized(self):
        email="test@GMAIL.COM"
        user=get_user_model().objects.create_user(
        email=email,password="test123"
        )

        self.assertEqual(email.lower(),user.email)


    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')


    def test_create_new_superuser(self):
        user=get_user_model().objects.create_superuser(
        'neelkk@gmail.com',
        'arc123'

        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag=models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag),tag.name)

    def test_ingredient_str(self):
        ingredient=models.Ingredient.objects.create(
        user=sample_user(),
        name='Cucumber'
        )
        self.assertEqual(str(ingredient),ingredient.name)

    def test_recipe_str(self):
        recipe=models.Recipe.objects.create(
            user=sample_user(),title='Steak',
            time_minutes=5,price=5.00
        )
