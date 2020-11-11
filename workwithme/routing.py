from django.conf.urls import url
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from message.consumers import ChatConsumer
from  notifications import routing as notification_routing
from notifications.consumer import NotificationConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
    	AuthMiddlewareStack(
    		URLRouter(
 				[
 					url(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer),
					#notification_routing.websocket_urlpatterns,
					path('ws/notification/<int:user_id>/',NotificationConsumer),
 				]
    		)
    	)
    )
})