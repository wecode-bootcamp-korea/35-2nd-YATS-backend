from django.http  import JsonResponse
from django.views import View
from django.db.models import Q, Max, Min, Count, Prefetch

import pandas as pd

from .models      import Stay, StayImage, Room , RoomOption
from books.models import Book

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

class RoomDetailView(View):
    def get(self, request, room_name):
        try:
            room = Room.objects.prefetch_related(
                'features',
                'add_ons',
                'amenities',
                'roomoption_set'
            ).get(name=room_name)
                
            result  = [{
                'room_name'   : room.name,
                'content'     : room.content,
                'checkin'     : room.checkin,
                'checkout'    : room.checkout,
                'max_capacity': room.max_capacity,
                'min_capacity': room.min_capacity,
                'area'        : room.area,
                'bed'         : room.bed,
                'features'    : [{
                    'id'  : feature.id,
                    'name': feature.name,
                    'icon': feature.icon
                    } for feature in room.features.all()],
                'amenities' : [{
                    'id'  : amenity.id,
                    'name': amenity.name,
                    } for amenity in room.amenities.all()],
                'add_ons' : [{
                    'id'  : addon.id,
                    'name': addon.name
                    } for addon in room.add_ons.all()],
            }]
                
            faq = {
                'room_name'   : room.name,
                'min_capacity': room.min_capacity,
                'max_capacity': room.max_capacity,
                'price'       : [{
                    option.option.season: option.price
                }for option in room.roomoption_set.all()]
            }

            return JsonResponse({'result' : result, 'FAQ' : faq}, status=200)

        except Room.DoesNotExist: 
            return JsonResponse({'message' : 'Dose Not Exist'}, status=404)


class FindStayView(View):
    def get(self, request):
        try:
            address    = request.GET.get('address', None)
            region     = request.GET.get('region' , None)
            checkin    = request.GET.get('checkin', None)
            checkout   = request.GET.get('checkout', None)
            people_cnt = request.GET.get('people_cnt', None)
            min_price  = request.GET.get('min_price', None)
            max_price  = request.GET.get('max_price', None)
            sorting    = request.GET.get('sort', None)
            offset     = int(request.GET.get('offset', 0))
            limit      = int(request.GET.get('limit', 6))

            filter_options = {
                'stay_type' : 'stay_type__name__in',
                'themes'    : 'themes__name__in'
            }

            filter_set = {
                filter_options.get(key) : value for (key, value) in dict(request.GET).items() if filter_options.get(key)
            }

            searchfilter = Q()
            bookdate     = Q()

            if address:
                searchfilter &= Q(address__icontains=address)

            if region:
                searchfilter &= Q(address__startswith=region)
            
            if people_cnt:
                searchfilter &= Q(room__min_capacity__lte=people_cnt, room__max_capacity__gte=people_cnt)
            
            if min_price:
                searchfilter &= Q(room__roomoption__price__gte=min_price)

            if max_price:
                searchfilter &= Q(room__roomoption__price__lte=max_price)
            
            if checkin and checkout:
                books          = Book.objects.all()
                lookupdate     = pd.date_range(checkin, checkout) 
                lookupdatelist = lookupdate.strftime("%Y%m%d").tolist()
                
                for book in books:
                    reserveddate     = pd.date_range(book.check_in, book.check_out)
                    reserveddatelist = reserveddate.strftime("%Y%m%d").tolist()
                    
                    if set(lookupdatelist) & set(reserveddatelist):
                        bookdate |= Q(room__book__id=book.id)

            sort = {
                None         : 'id',
                'created_at' : '-created_at',
                'high_price' : 'high_price',
                'low_price'  : 'low_price',
                'popular'    : '-count'
            }

            totalstay = (
                Stay.objects
                .select_related('stay_type')
                .annotate(
                    low_price  = Min('room__roomoption__price'),
                    high_price = Max('room__roomoption__price'),
                    count      = Count('room__book')
                ) 
                .filter(searchfilter, **filter_set)
                .exclude(bookdate)
                .order_by(sort[sorting])
                .prefetch_related(
                    Prefetch('stayimage_set', StayImage.objects.all(), to_attr='stayimages'),
                    Prefetch('room_set', Room.objects.all(), to_attr='rooms'),
                    Prefetch('rooms__roomoption_set', RoomOption.objects.all(), to_attr="roomoptions"),
                )    
            )
            
            stays = totalstay[offset:offset+limit]
            
            count = len(totalstay)

            result  = [{
                    'stay_id'        : stay.id,
                    'stay_name'      : stay.name,
                    'stay_type'      : stay.stay_type.name,
                    'stay_latitude'  : stay.latitude,
                    'stay_longitude' : stay.longitude,
                    'stay_address'   : {'stay_region' : stay.address[:2], 'stay_district' : stay.address.split()[1]},
                    'stay_price'     : {'low_price' : stay.low_price, 'high_price' : stay.high_price},
                    'stay_capacitiy' : stay.room_set.aggregate(min_capacity=Min('min_capacity'),max_capacity=Max('max_capacity')),
                    'stay_image'     : [{'id': image.id, 'url' : image.image }for image in stay.stayimages]
                } for stay in stays]

            return JsonResponse({'result' : result, 'totalcount': count}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY ERROR'}, status=400)
