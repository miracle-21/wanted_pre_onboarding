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

        title = data['title']
        content = data['content']
        position = data['position']
        compensation = data['compensation']
        skill = data['skill']

        Announcement.objects.create(
            company_id = request.company.id,
            title = title,
            content = content,
            position = position,
            compensation = compensation,
            skill = skill
        )

        return JsonResponse({'message' : 'Create Announcement'}, status = 201)

class GetView(View):
    def get(self, request):
        search = request.GET.get('search')

        q = Q()

        if search:
            q &= Q(company__name__contains = search) | Q(position__contains = search) | Q(skill__contains = search)

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

class DeleteView(View):
    @token_company
    def delete(self, request, announcement_id):
        try:
            announcement = Announcement.objects.get(id=announcement_id)
            if announcement.company_id == request.company.id:
                announcement.delete()

                return JsonResponse({'message' : 'Delete Complite'}, status = 200)
            else:
                return JsonResponse({'message' : 'Invalid Company'}, status = 401)
        except Announcement.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Announcement'}, status = 401)
       

class UpdateView(View):
    @token_company
    def patch(self, request, announcement_id):
        try:
            announcement = Announcement.objects.get(id=announcement_id)
            
            if announcement.company_id == request.company.id:
                data = json.loads(request.body) 
                announcement = Announcement.objects.get(id = announcement_id)

                if 'title' in data.keys():
                    announcement.title = data['title']
                if 'content' in data.keys():
                    announcement.content = data['content']
                if 'position' in data.keys():
                    announcement.position = data['position']
                if 'compensation' in data.keys():
                    announcement.compensation = data['compensation']
                if 'skill' in data.keys():
                    announcement.skill = data['skill']
                
                announcement.save()

                return JsonResponse({'message' : 'Update Complite'}, status = 200)
            else:
                return JsonResponse({'message' : 'Invalid Company'}, status = 401)
        except Announcement.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Announcement'}, status = 401)

class DetailView(View):
    def get(self, request):
        results = [
            {
                'announcement_id' : announcement.id,
                'company' : announcement.company.name,
                'title' : announcement.title,
                'content' : announcement.content,
                'position' : announcement.position,
                'compensation' : int(announcement.compensation),
                'skill' : announcement.skill,
                'other announcement_id' : [i.id for i in Announcement.objects.filter(company_id=announcement.company.id)]

            } for announcement in Announcement.objects.all()
        ]
        return JsonResponse({'results' : results}, status = 200)