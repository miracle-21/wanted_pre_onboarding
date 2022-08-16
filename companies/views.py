import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.conf import settings

from core.validation import validate_password
from companies.models import Company

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name = data['name']
            nation = data['nation']
            region = data['region']
            password = data['password']

            if Company.objects.filter(name=name).exists():
                return JsonResponse({'message' : 'Registered Company'}, status=409)
            
            validate_password(password)

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            Company.objects.create(
                name = name,
                nation = nation,
                region = region,
                password = hashed_password.decode('utf-8')
            )

            return JsonResponse({'message' :'Registration Success'}, status = 201)
        except ValidationError as error:
            return JsonResponse({'message' : error.message}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            company = Company.objects.get(name=data['name'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), company.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

            access_token = jwt.encode({"id" : company.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({'access_token' : access_token}, status = 200)
            
        except Company.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Company'}, status = 401)