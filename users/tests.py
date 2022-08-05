import jwt

from unittest.mock import patch, MagicMock

from django.test import Client, TestCase
from django.conf import settings

from users.models import User

class KakaoTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            kakao_id = 12345678,
            nickname = 'bawool',
            email    = 'bawool@gmail.com'
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_success_kakao_exist_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
	                    'id'          : 12345678,
	                    'connected_at': '2022-08-04T09:05:45Z',
	                    'properties'  : {
                            'nickname': 'bawool'
                            },
 	                    'kakao_account': {
                             'profile_nickname_needs_agreement': False,
                             'profile'                         : {'nickname': 'bawool'},
                             'has_email'                       : True,
                             'email_needs_agreement'           : False,
                             'is_email_valid'                  : True,
                             'is_email_verified'               : True,
                             'email'                           : 'bawool@gmail.com'
                             }
                        }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Athorization': '12345678'}
        response            = client.get('/users/kakao', **headers)
        token               = jwt.encode({'id': User.objects.get(id=1).id}, settings.SECRET_KEY, settings.ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'message': 'LOGIN',
            'token'  : token
        })

    @patch('users.views.requests')
    def test_success_kakao_new_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
	                    'id'          : 123456789,
	                    'connected_at': '2022-08-04T09:05:45Z',
	                    'properties'  : {
                            'nickname': 'test'
                            },
 	                    'kakao_account': {
                             'profile_nickname_needs_agreement': False,
                             'profile'                         : {'nickname': 'test'},
                             'has_email'                       : True,
                             'email_needs_agreement'           : False,
                             'is_email_valid'                  : True,
                             'is_email_verified'               : True,
                             'email'                           : 'test@gmail.com'
                             }
                        }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Athorization': '12345678'}
        response            = client.get('/users/kakao', **headers)
        token               = jwt.encode({'id': User.objects.latest('id').id}, settings.SECRET_KEY, settings.ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            'message': 'FIRSTLOGIN',
            'token'  : token
        })