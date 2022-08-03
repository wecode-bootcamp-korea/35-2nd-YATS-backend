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
                    checkout     = '11:00',                                   
                    checkin      = '16:00',
                    area         = 76,                                        
                    bed          = '1개',
                    stay_id      = 1111,                                      
                    room_type_id = 1111,
                    ),
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
            ]
        )
        
        RoomImage.objects.bulk_create(
            [
                RoomImage(id=1111, image='roomimage1', room_id=1111),
                RoomImage(id=1112, image='roomimage2', room_id=1111),
                RoomImage(id=1113, image='roomimage3', room_id=1111),
                RoomImage(id=1114, image='roomimage4', room_id=1111),
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
                    ],
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

    def test_roomdetailview_get_succees(self): 
        client = Client()

        response = client.get('/room/room%20A1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            "result"  : [{
                'room_name'   : 'room A1',
                'content'     : "Room A 1 is on the 1st floor with an ou",
                'checkin'     : '16:00',
                'checkout'    : '11:00',
                "max_capacity": 3,
                "min_capacity": 1,
                "area"        : "76.00",
                "bed"         : "1개",
                "features"    : [
                    {
                        "id"  : 1111,
                        "name": "a",
                        "icon": "a"
                    },
                    {
                        "id"  : 1112,
                        "name": "b",
                        "icon": "b"
                    },
                    {
                        "id"  : 1113,
                        "name": "c",
                        "icon": "c"
                    }
                ],
                "amenities": [
                    {
                        "id"  : 1111,
                        "name": "a"
                    },
                    {
                        "id"  : 1112,
                        "name": "b"
                    },
                    {
                        "id"  : 1113,
                        "name": "c"
                    }
                ],
                "add_ons": [
                    {
                        "id"  : 1111,
                        "name": "a"
                    },
                    {
                        "id"  : 1112,
                        "name": "b"
                    },
                    {
                        "id"  : 1113,
                        "name": "c"
                    },
                ],
            }],

            "FAQ": {
                    "room_name"   : "room A1",
                    "min_capacity": 1,
                    "max_capacity": 3,
                    "price"       : [
                        {
                            "평일": "2000000.00"
                        },
                        {
                            "주말": "2200000.00"
                        },
                        {
                            "성수기": "2400000.00"
                        },
                    ]
                }
            }
        )

        def test_staylistview_get_succees(self):
            client = Client()

            response = client.get('/findstay')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),
                {
                    "result": [
                        {
                        "stay_id"        : 1,
                        "stay_name"      : "monogarden",
                        "stay_type"      : "RENTAL HOUSE",
                        "stay_latitude"  : "126.3023260000",
                        "stay_longitude" : "33.4482913000",
                        "stay_address"   : {
                            "stay_region"   : "제주",
                            "stay_district" : "서귀포시"
                        },
                        "stay_price" : {
                            "low_price"  : "2000000.00",
                            "high_price" : "2900000.00"
                        },
                        "stay_capacitiy" : {
                            "min_capacity" : 1,
                            "max_capacity" : 3
                        },
                        "stay_image" : [
                            {"id" : 1, "url" : "stayImage1"},
                            {"id" : 2, "url" : "stayImage2"},
                            {"id" : 3, "url" : "stayImage3"},
                        ]
                    }], "totalcount" : 1
                }
            )