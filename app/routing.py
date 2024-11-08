from django.urls import re_path, path

from .channels import GameJoinAndLeave, WatchGameJoinAndLeave

websocket_urlpatterns = [
    path('game/<int:game_id>/', GameJoinAndLeave.as_asgi()),
    path('game-save/<int:game_id>/', WatchGameJoinAndLeave.as_asgi()),
]
