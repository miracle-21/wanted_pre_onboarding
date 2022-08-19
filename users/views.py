import json
import bcrypt
import jwt

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from django.conf import settings

from core.validation import validate_email, validate_password
from core.token import token_user
from users.models    import User, Apply
from companies.models import Announcement

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']
            name = data['name']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'Registered User'}, status=409)

            validate_email(email)
            validate_password(password)

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            User.objects.create(
                name  = name,
                email = email,
                password  = hashed_password.decode('utf-8')
            )
            return JsonResponse({'message' :'Registration Complite'}, status = 201)
        except ValidationError as error:
            return JsonResponse({'message' : error.message}, status = 400)

class SignInView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)
            
            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'Invalid User'}, status = 401)

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({'message' : 'Login Complete'}, headers = {'access_token' : access_token}, status = 200)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'Invalid User'}, status = 401)

class UserView(View):
    @token_user
    def post(self, request, announcement_id):
        try:
            announcement = Announcement.objects.get(id = announcement_id)
            user = request.user

            apply, is_created = Apply.objects.get_or_create(announcement = announcement, user = user)

            if not is_created:
                apply.delete()
                return JsonResponse({'message' : 'Apply Deleted'}, status = 204)

            return JsonResponse({'message' : 'Apply'}, status = 201)

        except Announcement.DoesNotExist:
            return JsonResponse({'message' :'Invalid Announcement'}, status = 401)