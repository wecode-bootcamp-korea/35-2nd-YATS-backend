import json
import uuid
from datetime import datetime

from django.http import JsonResponse
from django.views import View

from core.utils   import login_decorator   
from books.models import Book, BookStatus
from stays.models import *


class BookView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try: 
            user           = request.user
            room_id        = data['room_id']
            check_in       = data['check_in']   
            check_out      = data['check_out']
            check_in_date  = datetime.strptime(check_in,'%Y-%m-%d')
            check_out_date = datetime.strptime(check_out,'%Y-%m-%d')

            room   = Room.objects.get(id=room_id)
            status = BookStatus.objects.get(id=1)   

            Book.objects.create(
                book_number = uuid.uuid4().hex,
                status      = status,
                user        = user,
                room        = room,  
                check_in    = check_in_date,
                check_out   = check_out_date
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Room.DoesNotExist:
            return JsonResponse({'message': 'INVALID_ROOM_ID'}, status=400)

    @login_decorator
    def get(self, request):
        user      = request.user
        status_id = request.GET.get('status_id', 1)
        books     = Book.objects.filter(user=user, status_id=status_id)

        user_result = {
                'name'         : user.nickname,
                'email'        : user.email           
        }
        results = [{
                'book_number'  : book.book_number,
                'room_name'    : book.room.name,
                'check_in'     : book.check_in,
                'check_out'    : book.check_out,
                'status'       : book.status.status,
                'booked_date'  : book.created_at,
                'canceled_date': book.updated_at,
                'stay_type'    : book.room.stay.stay_type.name,
                'stay_address' : {'stay_region' : book.room.stay.address[:2], 'stay_district' : book.room.stay.address.split()[1]},
                'stay_price'   : {'low_price': RoomOption.objects.get(room=book.room,option_id=1).price, 
                                  'high_price': RoomOption.objects.get(room=book.room,option_id=3).price},
                'stay_capacity': {'min_capacity': book.room.min_capacity , 'max_capacity': book.room.max_capacity},
                'room_image'   : RoomImage.objects.filter(room=book.room)[0].image
            }for book in books]

        return JsonResponse({'message': 'SUCCESS', 'user_data': user_result,'results': results}, status=200)

        # results = [{
        #         'name'         : user.korean_name,
        #         'email'        : user.email,
        #         'book_number'  : book.book_number,
        #         'room_name'    : book.room.name,
        #         'check_in'     : book.check_in,
        #         'check_out'    : book.check_out,
        #         'status'       : book.status.status,
        #         'booked_date'  : book.created_at,
        #         'canceled_date': book.updated_at
        #     }for book in books]

        # return JsonResponse({'message': 'SUCCESS', 'results': results}, status=200)

class CancelView(View):
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user        = request.user
            book_number = data['book_number']

            Book.objects.filter(user=user, book_number=book_number).update(status_id = 2)
        
        except Book.DoesNotExist:
            return JsonResponse({'message': 'INVALID_BOOK_NUMBER'}, status=404)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)