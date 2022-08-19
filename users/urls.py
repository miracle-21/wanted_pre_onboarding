from django.urls import path

from users.views import *
urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/<int:announcement_id>', UserView.as_view()),
]
