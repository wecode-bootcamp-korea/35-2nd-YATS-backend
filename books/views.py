import json
import uuid
from datetime import datetime

from django.http import JsonResponse
from django.views import View

from core.utils   import login_decorator   
from books.models import Book, BookStatus
from stays.models import Room


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

            room   = Room.objects.get(room_id=room_id)
            status = BookStatus.objects.get(id=1),   

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