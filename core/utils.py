import jwt, uuid

from django.conf import settings
from django.http import JsonResponse

from users.models import User

def login_decorator(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token,settings.SECRET_KEY, settings.ALGORITHM)
            user_id      = payload['user_id']
            request.user = User.objects.get(id=user_id)
            return func(self, request)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
    return wrapper


class ImageUploader:
    def __init__(self, client):
        self.client = client

    def upload(self, file):
        image_name = str(uuid.uuid4())
        self.client.upload_fileobj(
                    file, 
                    "yatsbucket",
                    image_name,
                    ExtraArgs={
                        "ContentType": file.content_type
                    }
                )
        return 'https://yatsbucket.s3.ap-northeast-2.amazonaws.com/' + image_name,   

class ImageHandler:
    def __init__(self, client, file):
        self.client = client
        self.file   = file

    def save(self):
        return self.client.upload(self.file)