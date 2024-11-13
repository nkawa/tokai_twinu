from channels.generic.websocket import AsyncWebsocketConsumer
import json
import socketio

import sys
sys.path.append("sims/core/")
#print(sys.path)

#from webstart import doit
import webstart

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)


@sio.on('MyEvent')
#async def receive_event(sid, message):
async def receive_event(*args):
    print("MyEvent!",args)
    if len(args)>=2:
        if args[1]=="Doit":
            await webstart.doit(sio)
        elif args[1]=='stop':
            await webstart.stop(sio)
        elif args[1]=='addTruck':
            await webstart.addTruck()
        elif args[1]=='showRoads':
            await webstart.showRoads()


#        await sio.emit('event',{'i':0,'height':9.0})
#    await sio.emit('my response', {'data': message['data']}, r  oom=sid)


@sio.on('my broadcast event', namespace='/test')
async def test_broadcast_message(sid, message):
    await sio.emit('my response', {'data': message['data']}, namespace='/test')


@sio.on('join', namespace='/test')
async def join(sid, message):
    sio.enter_room(sid, message['room'], namespace='/test')
    await sio.emit('my response', {'data': 'Entered room: ' + message['room']},
                   room=sid, namespace='/test')


@sio.on('leave', namespace='/test')
async def leave(sid, message):
    sio.leave_room(sid, message['room'], namespace='/test')
    await sio.emit('my response', {'data': 'Left room: ' + message['room']},
                   room=sid, namespace='/test')


@sio.on('close room', namespace='/test')
async def close(sid, message):
    await sio.emit('my response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'], namespace='/test')
    await sio.close_room(message['room'], namespace='/test')


@sio.on('my room event', namespace='/test')
async def send_room_message(sid, message):
    await sio.emit('my response', {'data': message['data']},
                   room=message['room'], namespace='/test')


@sio.on('disconnect request')
async def disconnect_request(sid):
    print("Disconnect request")
    await sio.disconnect(sid)


@sio.on('connect')
async def connected(sid, environ):
    pass
    print("Connected!")#,sid,environ)


@sio.on('disconnect')
def disconnected(sid):
    print('Client disconnected')#,sid)

