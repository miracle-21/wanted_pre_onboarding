import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Q

from core.token import token_company
from core.validation import validate_password
from companies.models import Company, Announcement

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

            return JsonResponse({'message' :'Registration Complite'}, status = 201)
        except ValidationError as error:
            return JsonResponse({'message' : error.message}, status = 400)

class SignInView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)
            company = Company.objects.get(name=data['name'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), company.password.encode('utf-8')):
                return JsonResponse({'message' : 'Invalid Company'}, status = 401)

            access_token = jwt.encode({"id" : company.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({'message' : 'Login Complete'}, headers = {'access_token' : access_token}, status = 200)
            
        except Company.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Company'}, status = 401)

class CreateView(View):
    @token_company
    def post(self, request):
        data = json.loads(request.body)

        company = data['company']
        title = data['title']
        content = data['content']
        position = data['position']
        compensation = data['compensation']
        skill = data['skill']

        Announcement.objects.create(
            company_id = Company.objects.get(name=company).id,
            title = title,
            content = content,
            position = position,
            compensation = compensation,
            skill = skill
        )

        return JsonResponse({'message' : 'Create Announcement'}, status = 201)

class GetView(View):
    @token_company
    def get(self, request):
        search = request.GET.get('search')

        q = Q()

        if search:
            q &= (Q(company__name__contains = search) | Q(position__contains = search) | Q(skill__contains = search))

        announcements = Announcement.objects.filter(q)

        results = [
            {
                'announcement_id' : announcement.id,
                'company' : announcement.company.name,
                'title' : announcement.title,
                'content' : announcement.content,
                'position' : announcement.position,
                'compensation' : int(announcement.compensation),
                'skill' : announcement.skill
            } for announcement in announcements
        ]
        return JsonResponse({'results' : results}, status = 200)


        # title = request.body.get('title')
        # content = request.body.get('content')
        # position = request.body.get('position')
        # compensation = request.body.get('compensation')
        # skill = request.body.get('skill')

        # a.title = title
        # a.content = content
        # a.position = position
        # a.compensation = compensation
        # a.skill = skill

        # a.save()

        # return JsonResponse({'message' : 'Update Announcement'}, status = 201)


