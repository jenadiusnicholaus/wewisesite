import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

from message.models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		print("connected",event)
		await self.send({
			"type":"websocket.accept"
		})
		other_user = self.scope['url_route']['kwargs']['username']
		me = self.scope['user']
		t_obj = await self.get_thread(me, other_user)
		self.t_obj = t_obj
		chat_room = f'thread_{t_obj.id}'
		self.chat_room = chat_room
		await self.channel_layer.group_add(
			chat_room,
			self.channel_name
		)
    

	async def websocket_receive(self, event):
		print("receieve",event)
		front_text =  event.get('text', None)
		if front_text is not None:
			loaded_data = json.loads(front_text)
			msg = loaded_data.get('message')
			print(msg)
			user = self.scope['user']
			username = 'default'
			if user.is_authenticated:
				username = user.username
			myResponse = {
				'message':msg,
				'username': username
			}
			await self.create_chat_messages(user, msg)
			await self.channel_layer.group_send(
				self.chat_room,
				{
				  "type":"chat_message",
				  "text":json.dumps(myResponse)
				}
		   )
		   
	async def chat_message(self, event):
		print('message', event)
		await self.send({
			"type":"websocket.send",
			"text":event['text']
		})


	async def websocket_disconnect(self, event):
		print("disconnected",event)
		


	@database_sync_to_async
	def get_thread(self, user, other_username):
		return Thread.objects.get_or_new(user, other_username)[0]


	@database_sync_to_async
	def create_chat_messages(self, me, msg):
		t_obj = self.t_obj
		return ChatMessage.objects.create(user=me, thread=t_obj, message=msg)
