import jwt

from django.http import JsonResponse

from companies.models import Company
from wanted.settings import SECRET_KEY, ALGORITHM

def token_company(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            company = Company.objects.get(id=payload['id'])
            request.company = company
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'Invalid Token'}, status=401)

        except Company.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Company'}, status=401)

    return wrapper