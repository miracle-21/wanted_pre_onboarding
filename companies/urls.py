from django.urls import path

from companies.views import *
urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/post', CreateView.as_view()),
    path('/get', GetView.as_view()),
    path('/delete/<int:announcement_id>', DeleteView.as_view()),
    path('/update/<int:announcement_id>', UpdateView.as_view()),
    path('', DetailView.as_view()),
]