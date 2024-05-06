
from django.contrib import admin
from django.urls import path, include
from llama3.views import get_llama3 as llama3
# from llama3.views import chat_view
# from llama3.views import chat_html
from webai.views import chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('wechatapp.urls'), name='wechatapp'),
    # path('chat/', chat_view, name='chat'),
    # path('index/', chat_html, name='index'),
    # path('chat/', chat_view, name='chat'),
    path('api/v1/', include('webai.urls'), name='webai')
]
