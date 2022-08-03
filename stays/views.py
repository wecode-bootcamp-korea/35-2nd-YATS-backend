from django.http  import JsonResponse
from django.views import View
from django.db.models import Min, Max, Prefetch

from .models import RoomOption, Stay, StayImage, Room

class StayDetailView(View):
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