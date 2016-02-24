#!/usr/bin/env python

import tornado.ioloop 
import tornado.web 

import asyncio
import websockets
import tornado.platform.asyncio
tornado.platform.asyncio.AsyncIOMainLoop().install()



class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("./views/index.html", title = "GPS")

def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
	])

app = make_app()
app.listen(8888)
print("APP is listening on *8888")

clients = []

async def hello(websocket, path):
	clients.append(websocket)
	
	while True:
		name = await websocket.recv()
		print("< {}".format(name))
		
		print(clients)
		greeting = "Hello {}!".format(name)
		for each in clients:
			await each.send(greeting)
			print("> {}".format(greeting))

start_server = websockets.serve(hello, 'localhost', 8765)
print("Listening on *8765")





asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()