import json

from django.http import JsonResponse
from django.views import View

from core.utils   import login_decorator
from likes.models import Like
from stays.models import Stay


class LikeView(View):
    @login_decorator
    def post(self,request):
        try:
            data    = json.loads(request.body)
            stay_id = data['stay_id']
            user    = request.user
            stay    = Stay.objects.get(id=stay_id)

            like, is_created = Like.objects.get_or_create(
                stay = stay,
                user = user
            )

            if not is_created :
                like.delete()           

            return JsonResponse({'message': 'SUCCESS', 'result': is_created}, status=200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Stay.DoesNotExist:
            return JsonResponse({'message': 'INVALID_STAY'}, status=404)
            
    @login_decorator
    def get(self, request):
        user = request.user

        likes = Like.objects.filter(user=user).select_related("stay")

        results = [{
            'stay_id'  : like.stay.id,
            'stay_name': like.stay.name,
            'address'  : like.stay.address
            } for like in likes]

        return JsonResponse({'message': 'SUCCESS', 'results': results}, status=200)
            

