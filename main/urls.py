from django.urls import path
from .views import landing_page, main_page, upload_file_view

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('chat', main_page, name='main_page'),
    path('upload', upload_file_view, name='upload_file')
]