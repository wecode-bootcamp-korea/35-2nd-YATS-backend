import jwt

from django.test import TestCase, Client
from django.conf import settings

from likes.models import Like
from users.models import User
from stays.models import Stay, StayType

class LikeTest(TestCase):

    def setUp(self):
        User.objects.create(
            id           = 1,
            email        = 'example@gmail.com',
            korean_name  = '홍길동',
            phone_number = '010-1111-2222',
            nickname     = 'EastWest'
        )
        
        StayType.objects.create(
            id   = 1,
            name = '펜션'
        )
        StayType.objects.create(
            id   = 2,
            name = '한옥'
        )    

        Stay.objects.create(
            id             = 1,
            name           = '스테이디',
            address        = '서울시 양천구 목동중앙북로 38',
            latitude       = 37.548850, 
            longitude      = 126.866717,
            keyword        = '돌담이 품어준 우리의 쉼터',
            summary        = '진한 쉼과 가장 서울다운 추억을 새기다.',
            content_top    = '비로소 흥성하는 마을’이라는 뜻을 품고 있는 이 마을은 우도, 일출봉, 두산봉, 지미봉 등으로 둘러싸인 조용한 마을입니다.',
            content_bottom = '스테이 아린은 여러 갈래 길이 모이는 위치에 자리하고 있어 접근성이 좋습니다.',
            phone_number   = '0504-0904-2603',
            email          = 'stayarin0204@gmail.com',
            stay_type      = StayType.objects.get(id=1)
        )
        Stay.objects.create(
            id             = 2,
            name           = '오후 다섯시',
            address        = '경기도 부천시 역곡로 97',
            latitude       = 37.644459,
            longitude      = 126.850621,
            keyword        = '아스라히 스러지는 달이 아름다운 공간',
            summary        = '흘러가는 그대로 머무르는 시간',
            content_top    = '이곳에는 아침부터 저녁까지 각양각색의 볕이 모든 공간에 스며듭니다.',
            content_bottom = '느긋한 고양이가 놀러 와 시간을 보내기도 합니다',
            phone_number   = '0504-0904-2588',
            email          = 'catsofsummer@naver.com',
            stay_type      = StayType.objects.get(id=2)
        )

        Like.objects.create(
            user = User.objects.get(id=1),
            stay = Stay.objects.get(id=2)
        )

    def tearDown(self):
        User.objects.all().delete()
        Stay.objects.all().delete()
        StayType.objects.all().delete()
        Like.objects.all().delete()

    def test_success_likeview_post_create_data(self):
        client = Client()
        data = {'stay_id' :1 }
        access_token = jwt.encode( {'user_id': 1}, settings.SECRET_KEY, settings.ALGORITHM  )
        headers = {'HTTP_Authorization': access_token}
        response = client.post('/likes', data=data, **headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'result': True})

    def test_success_likeview_post_delete_data(self):
        client = Client()
        data = {'stay_id': 2}
        access_token = jwt.encode( {'user_id': 1}, settings.SECRET_KEY, settings.ALGORITHM  )
        headers = {'HTTP_Authorization': access_token}
        response = client.post('/likes', data=data, **headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'result': False})


    def test_fail_likeview_post_create_data_key_error(self):
        client = Client()
        data = {'stay': 1}
        access_token = jwt.encode( {'user_id': 1}, settings.SECRET_KEY, settings.ALGORITHM  )
        headers = {'HTTP_Authorization': access_token}
        response = client.post('/likes', data=data, **headers, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

    def test_fail_likeview_post_create_data_stay_doesnotexit(self):
        client = Client()
        data = {'stay_id': 8000}
        access_token = jwt.encode( {'user_id': 1}, settings.SECRET_KEY, settings.ALGORITHM  )
        headers = {'HTTP_Authorization': access_token}
        response = client.post('/likes', data=data, **headers, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'INVALID_STAY'})


