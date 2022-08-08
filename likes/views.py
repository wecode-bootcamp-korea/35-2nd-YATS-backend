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

