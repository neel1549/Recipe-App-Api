from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from coreapp.models import Tag
from recipe.serializers import TagSerializer

TAG_URL='recipe:tag-list'
class PublicTagsApiTests(TestCase):

    def setUp(self):
        self.client=APIClient()

    def test_login_required(self):
        res=self.client.get(TAG_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):

    def setUp(self):
        self.user=get_user_model().objects.create_user(
            'neelk@gmail.com',
            'test123'

        )
        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user,name='Vegan')
        Tag.objects.create(user=self.user,name='Dessert')
        res=self.client.get(TAG_URL)

        tags=Tags.objects.all().orderby("-name")
        serializer=TagSerializer(tags,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)


    def test_tags_limited_to_user(self):
        user2=get_user_model().objects.create_user(
        'other@gmail.com','gd1234'

        )
        Tag.objects.create(user=user2,name='Fruity')
        tag=Tag.objects.create(user=self.user,name='Comfort_Food')
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],tag.name)

    def test_create_tags_successful(self):
        payload={'Name':'Test_Tag'}
        self.client.post(TAG_URL,payload)
        exists=Tag.objects.filter(
        user=self.user,
        name=payload['Name']
        )
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        payload={'Name':''}
        res=self.client.post(TAG_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
