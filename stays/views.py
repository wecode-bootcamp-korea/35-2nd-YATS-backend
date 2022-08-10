import boto3
import uuid

from django.conf  import settings
from django.http  import JsonResponse
from django.views import View
from django.db.models import Min, Max, Prefetch

from stays.models import StayType, Theme, Stay, StayImage, RoomType, RoomImage, RoomOption, Room, AddOn, Amenity, Feature
from core.utils   import ImageUploader, ImageHandler

class StayDetailView(View):
    """
    OOP 적용-!
    """
    def get(self, request, stay_id):
        try:
            stay = Stay.objects.select_related(
                'stay_type',
                ).annotate(
                minprice    = Min('room__roomoption__price'),
                maxprice    = Max('room__roomoption__price'),
                mincapacity = Min('room__min_capacity'),
                maxcapacity = Max('room__max_capacity'), 
                ).prefetch_related(
                    Prefetch('stayimage_set', StayImage.objects.all(), to_attr='stayimages'),
                    Prefetch('room_set', Room.objects.all(), to_attr='rooms'),
                    Prefetch('rooms__roomoption_set', RoomOption.objects.all(), to_attr="roomoptions"),                    
                ).get(id = stay_id)
                
            result  = [{
                'stay_id'      : stay.id,
                'stay_name'    : stay.name,
                'stay_image'   : [{
                    'id'  : image.id,
                    'url' : image.image
                    }for image in stay.stayimages],
                'stay_address' : {
                    'stay_region'   : stay.address[:2],
                    'stay_district' : stay.address.split()[1],
                    'stay_address'  : stay.address
                    },
                'stay_type'    : stay.stay_type.name,
                'stay_keyword' : stay.keyword,
                'stay_summary' : stay.summary,
                'stay_rooms'   : [{
                    'room_id'           : room.id,
                    'room_name'         : room.name,
                    'room_type'         : room.room_type.name,
                    'room_min_capacity' : room.min_capacity,
                    'room_max_capacity' : room.max_capacity,
                    'room_option'       : { roomoption.option.season : roomoption.price for roomoption in room.roomoptions},
                    'room_bad'          : room.bed,
                    'room_price'        : (room.roomoption_set.aggregate(price=Min('price')))['price']
                    } for room in stay.rooms],
                'stay_keyword'        : stay.keyword,
                'stay_summary'        : stay.summary,
                'stay_content_top'    : stay.content_top,
                'stay_content_bottom' : stay.content_bottom,
                'stay_feature'        : [{
                    'stay_feature_id'     : feature.id,
                    'stay_feature_name'   : feature.name,
                    'stay_feature_icon'   : feature.icon,
                    'stay_feature_detail' : feature.detail,
                } for feature in stay.themes.all()],
                'stay_mobile' : stay.phone_number,
                'stay_email'  : stay.email,
            }]

            return JsonResponse({'result' : result}, status=200)

        except Stay.DoesNotExist:
            return JsonResponse({'message' : 'Dose Not Exist'}, status=404)




s3_client = boto3.client(
        's3',
        aws_access_key_id     = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = settings.AWS_SCERET_ACCESS_KEY
    )

image_uploader = ImageUploader(s3_client)


class EnterView(View):
    def post(self, request):
        data = request.POST
        
        try: 
            stay_name       = data['stay_name']
            address         = data['address']
            latitude        = data['latitude']
            longitude       = data['longitude']
            keyword         = data['keyword']
            summary         = data['summary']
            content_top     = data['content_top']
            content_bottom  = data['content_bottom']
            phone_number    = data['phone']
            email           = data['email']
            stay_type_name  = data['types']
            stay_type       = StayType.objects.get(name=stay_type_name)
            theme_list      = data['themes']
            stay_image_list = request.FILES.getlist('stay_images')

            stay1 = Stay.objects.create(
                name           = stay_name,
                address        = address,
                latitude       = latitude,
                longitude      = longitude,
                keyword        = keyword,
                summary        = summary,
                content_top    = content_top,
                content_bottom = content_bottom,
                phone_number   = phone_number,
                email          = email,
                stay_type      = stay_type
            )
            for theme in theme_list:
                theme1 = Theme.objects.get(name=theme)
                theme1.stay.add(stay1)

            for stay_image in stay_image_list:
                image_handler = ImageHandler(image_uploader, stay_image)
                url           = image_handler.save()

                StayImage.objects.create(
                    image = url,
                    stay  = Stay.objects.get(name=stay_name)
                )

            rooms           = data['rooms']

            for room in rooms:
                add_on_list     = room['add_on']
                amenity_list    = room['amenity']
                feature_list    = room['feature']
                room_name       = room['room_name']
                room_type       = room['room_type']
                area            = room['area']
                bed             = room['bed']
                checkin         = room['checkin']
                checkout        = room['checkout']
                min_capacity    = room['min_capacity']
                max_capacity    = room['max_capacity']
                room_image_list = request.FILES.getlist('room_images')
                week_price      = room['week_price']
                weekend_price   = room['weekend_price']
                peek_price      = room['peek_price']
                price           = [week_price, weekend_price, peek_price]

                room1 = Room.objects.create(
                    name         = room_name,
                    content      = '거실, 침실, 주방, 화장실, 욕실, 세면실과 자쿠지로 구성되어 있습니다.',
                    min_capacity = min_capacity,
                    max_capacity = max_capacity,
                    checkin      = checkin,
                    checkout     = checkout,
                    area         = area,
                    bed          = bed,
                    stay         = stay1,
                    room_type    = RoomType.objects.get(name=room_type)
                )

                for room_image in room_image_list:
                    room_image_name = str(uuid.uuid4())
                    self.s3_client.upload_fileobj(
                        room_image, 
                        "yatsbucket",
                        room_image_name,
                        ExtraArgs={
                            "ContentType": room_image.content_type
                        }
                    ) 
                    RoomImage.objects.create(
                        image = 'https://yatsbucket.s3.ap-northeast-2.amazonaws.com/' + room_image_name,
                        room = Room.objects.get(name=room_name)
                    )

                bulk_list = []

                for i in range(len(rooms)):
                    bulk_list.append(RoomOption(room=room1, option_id=i+1, price=price[i]))
                    
                RoomOption.objects.bulk_create(bulk_list)

                for add_on in add_on_list:
                    add_on1 = AddOn.objects.get(name=add_on)
                    add_on1.room.add(room1)

                for amenity in amenity_list:
                    amenity1 = Amenity.objects.get(name=amenity)
                    amenity1.room.add(room1)

                for feature in feature_list:
                    feature1 = Feature.objects.get(name=feature)
                    feature1.room.add(room1)

            return JsonResponse({'message': 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

