from django.test import TestCase, Client
from django.contrib.auth import get_user_model


User = get_user_model()
client = Client()
# Create your tests here.


class StoreTestCast(TestCase):

    def setUp(self):
        user_a = User(username='thiane', email='thiane@code.com')
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.is_active = True
        user_a.set_password("thiane@1994")
        user_a.save()
        # store self.user_a to user_a along the test and can be reused
        self.user_a = user_a

        # store self.user_a_pw to "thiane@1994" along the test and can be reused
        self.user_a_pwd = "thiane@1994"

    def test_user_exist(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)

    def test_is_healthy(sefl):
        url = "/playground/health/"
        result = client.get(url)
        http_response = result.content.decode('utf-8')
        sefl.assertEqual(result.status_code, 200)
        sefl.assertEqual(http_response, 'running fine')

    def test_user_password(self):
        user_qs = User.objects.filter(username='thiane')
        user_a = user_qs.exists()
        self.assertTrue(user_a)
        self.assertTrue(self.user_a.check_password(self.user_a_pwd))
