from django.test import TestCase, Client

from .models import *
from books.models import Book, BookStatus
from users.models import User

class StayDetailTest(TestCase):

    def setUp(self):

        StayType.objects.create(id=1111, name='RENTAL HOUSE')

        Stay.objects.create(
            id             = 1111,
            name           = 'monogarden',
            address        = '제주특별자치도 서귀포시 성산읍 시흥하동로 52-4',
            latitude       = '126.302326',
            longitude      = '33.4482913',
            keyword        = 'A space of relaxation filled with dreams',
            summary        = 'A place where one can rest for a while, When one is tired of everyday life.',
            content_top    = 'Gwakji-gwamul Beach is famous for its beautiful scenery and Mono Garden has a bre',
            content_bottom = 'The Mono Garden buildings are Simba-Curry and Simba-Caf',
            phone_number   = '010-9006-4164',
            email          = 'monogarden_jeju@naver.com',
            stay_type_id   = 1111
        )

        StayImage.objects.bulk_create(
            [
                StayImage(id=1111, image='stayImage1', stay_id=1111),
                StayImage(id=1112, image='stayImage2', stay_id=1111),
                StayImage(id=1113, image='stayImage3', stay_id=1111)
            ]
        )

        Theme.objects.bulk_create(
            [
                Theme(id=1111, name='design', icon='monoicon1', detail='Furniture and props'),
                Theme(id=1112, name='design', icon='monoicon1', detail='Furniture and props'),
                Theme(id=1113, name='design', icon='monoicon1', detail='Furniture and props')
            ]
        )

        StayTheme.objects.bulk_create(
            [
                StayTheme(id=1111, stay_id=1111, theme_id=1111),
                StayTheme(id=1112, stay_id=1111, theme_id=1112),
                StayTheme(id=1113, stay_id=1111, theme_id=1113),
            ]
        )

        RoomType.objects.bulk_create(
            [
                RoomType(id=1111, name='Standard'),
                RoomType(id=1112, name='Duplex')
            ]
        )

        Room.objects.bulk_create(
            [
                Room(
                    id           = 1111,
                    name         = 'room A1',
                    content      = 'Room A 1 is on the 1st floor with an ou',
                    max_capacity = 3,                                         
                    min_capacity = 1,
                    checkout     = '16:00',                                   
                    checkin      = '11:00',
                    area         = 76,                                        
                    bed          = '1개',
                    stay_id      = 1111,                                      
                    room_type_id = 1111,
                    ),
                Room(
                    id           = 1112,
                    name         = 'room A1',
                    content      = 'Room A 1 is on the 1st floor with an ou',
                    max_capacity = 3,                                         
                    min_capacity = 1,
                    checkout     = '16:00',                                   
                    checkin      = '11:00',
                    area         = 76,                                        
                    bed          = '1개',
                    stay_id      = 1111,                                      
                    room_type_id = 1111,
                )
            ]
        )

        Feature.objects.bulk_create(
            [
                Feature(id=1111, name='a', icon='a'),
                Feature(id=1112, name='b', icon='b'),
                Feature(id=1113, name='c', icon='c'),
            ]
        )
        
        FeatureRoom.objects.bulk_create(
            [
                FeatureRoom(id=1111, feature_id=1111, room_id=1111),
                FeatureRoom(id=1112, feature_id=1112, room_id=1111),
                FeatureRoom(id=1113, feature_id=1113, room_id=1111),
                FeatureRoom(id=1114, feature_id=1111, room_id=1112),
                FeatureRoom(id=1115, feature_id=1112, room_id=1112),
                FeatureRoom(id=1116, feature_id=1113, room_id=1112)
            ]
        )
        
        Amenity.objects.bulk_create(
            [
                Amenity(id=1111, name='a'),
                Amenity(id=1112, name='b'),
                Amenity(id=1113, name='c'),
            ]
        )

        AmenityRoom.objects.bulk_create(
            [
                AmenityRoom(id=1111, amenity_id=1111, room_id=1111),
                AmenityRoom(id=1112, amenity_id=1112, room_id=1111),
                AmenityRoom(id=1113, amenity_id=1113, room_id=1111),
                AmenityRoom(id=1114, amenity_id=1111, room_id=1112),
                AmenityRoom(id=1115, amenity_id=1112, room_id=1112),
                AmenityRoom(id=1116, amenity_id=1113, room_id=1112),
            ]
        )

        AddOn.objects.bulk_create(
            [
                AddOn(id=1111, name='a',),
                AddOn(id=1112, name='b',),
                AddOn(id=1113, name='c',),
            ]
        )

        AddOnRoom.objects.bulk_create(
            [
                AddOnRoom(id=1111, addon_id=1111, room_id=1111),
                AddOnRoom(id=1112, addon_id=1112, room_id=1111),
                AddOnRoom(id=1113, addon_id=1113, room_id=1111),
                AddOnRoom(id=1114, addon_id=1111, room_id=1112),
                AddOnRoom(id=1115, addon_id=1112, room_id=1112),
                AddOnRoom(id=1116, addon_id=1113, room_id=1112),
            ]
        )

        
        Option.objects.bulk_create(
            [
                Option(id=1111, season='평일'),
                Option(id=1112, season='주말'),
                Option(id=1113, season='성수기')
            ]
        )

        RoomOption.objects.bulk_create(
            [
                RoomOption(id=1111, price=2000000, room_id=1111, option_id=1111),
                RoomOption(id=1112, price=2200000, room_id=1111, option_id=1112),
                RoomOption(id=1113, price=2400000, room_id=1111, option_id=1113),
                RoomOption(id=1114, price=2500000, room_id=1112, option_id=1111),
                RoomOption(id=1115, price=2700000, room_id=1112, option_id=1112),
                RoomOption(id=1116, price=2900000, room_id=1112, option_id=1113),
            ]
        )
        
        RoomImage.objects.bulk_create(
            [
                RoomImage(id=1111, image='roomimage1', room_id=1111),
                RoomImage(id=1112, image='roomimage2', room_id=1111),
                RoomImage(id=1113, image='roomimage3', room_id=1111),
                RoomImage(id=1114, image='roomimage4', room_id=1111),
                RoomImage(id=1115, image='roomimage5', room_id=1112),
                RoomImage(id=1116, image='roomimage6', room_id=1112),
                RoomImage(id=1117, image='roomimage7', room_id=1112),
                RoomImage(id=1118, image='roomimage8', room_id=1112),
            ]
        )
        
        User.objects.create(
            id           = 1111, 
            kakao_id     = 1234,
            korean_name  = 'leo',
            email        = 'leo1234@email.com',
            phone_number = '010-1234-2345',
            password     = 'leo1234!',
            nickname     = 'leo'
            )

        BookStatus.objects.bulk_create(
            [
                BookStatus(id=1111, status='에약중'),
                BookStatus(id=1112, status='취소됨'),
            ]
        )

        Book.objects.create(
            id          = 1111,
            book_number = '1234',
            check_in    = '2022-06-11',
            check_out   = '2022-06-13',
            status_id   = 1111,
            user_id     = 1111,
            room_id     = 1111
            ),
     
    def tearDown(self): 
        Stay.objects.all().delete()
        RoomOption.objects.all().delete()
        StayType.objects.all().delete()
        Room.objects.all().delete()
        Option.objects.all().delete()
        StayImage.objects.all().delete()
        Theme.objects.all().delete()
        RoomType.objects.all().delete()
        RoomImage.objects.all().delete() 
        User.objects.all().delete()
        BookStatus.objects.all().delete()
        Book.objects.all().delete() 
        AddOnRoom.objects.all().delete()
        AddOn.objects.all().delete()
        AmenityRoom.objects.all().delete()
        Amenity.objects.all().delete()
        FeatureRoom.objects.all().delete()
        Feature.objects.all().delete()
        StayTheme.objects.all().delete()
    
    def test_staydetailview_get_succees(self): 
        client = Client()
    
        response = client.get('/findstay/1111')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "result"  : [
                    {
                    'stay_id'     : 1111,
                    'stay_name'   : "monogarden",
                    'stay_image'  : [{'id': 1111, 'url': 'stayImage1'},{'id': 1112, 'url': 'stayImage2'},{'id': 1113, 'url': 'stayImage3'}],
                    'stay_address': {
                        'stay_region'  : "제주",
                        'stay_district': "서귀포시",
                        'stay_address' : "제주특별자치도 서귀포시 성산읍 시흥하동로 52-4",
                    },
                    'stay_type'   : "RENTAL HOUSE",
                    'stay_keyword': "A space of relaxation filled with dreams",
                    'stay_summary': "A place where one can rest for a while, When one is tired of everyday life",
                    'stay_rooms'  : [{
                        'room_id'          : 1111,
                        'room_name'        : "room A1",
                        'room_type'        : "Standard",
                        'room_min_capacity': 1,
                        'room_max_capacity': 3,
                        'room_option'      : { "평일" : "2000000.00", "주말" : "2200000.00", "성수기" : "2400000.00"},
                        'room_bad'         : "1개",
                        'room_price'       : "2000000.00",
                    },
                    {   
                        'room_id'          : 1112,
                        'room_name'        : "room A1",
                        'room_type'        : "Standard",
                        'room_min_capacity': 1,
                        'room_max_capacity': 3,
                        'room_option'      : { "평일" : "2500000.00", "주말" : "2700000.00", "성수기" : "2900000.00"},
                        'room_bad'         : "1개",
                        'room_price'       : "2500000.00",
                    }],
                    'stay_keyword'       : "A space of relaxation filled with dreams",
                    'stay_summary'       : "A place where one can rest for a while, When one is tired of everyday life.",
                    'stay_content_top'   : "Gwakji-gwamul Beach is famous for its beautiful scenery and Mono Garden has a bre",
                    'stay_content_bottom': "The Mono Garden buildings are Simba-Curry and Simba-Caf",
                    'stay_feature'       : [{
                        'stay_feature_id'    : 1111,
                        'stay_feature_name'  : "design",
                        'stay_feature_icon'  : "monoicon1",
                        'stay_feature_detail': "Furniture and props"
                    },
                    {
                        'stay_feature_id'    : 1112,
                        'stay_feature_name'  : "design",
                        'stay_feature_icon'  : "monoicon1",
                        'stay_feature_detail': "Furniture and props"
                    },
                    {
                        'stay_feature_id'    : 1113,
                        'stay_feature_name'  : "design",
                        'stay_feature_icon'  : "monoicon1",
                        'stay_feature_detail': "Furniture and props"
                    },
                    ],
                    'stay_mobile': "010-9006-4164",
                    'stay_email' : "monogarden_jeju@naver.com",
                    }]
                }
        )