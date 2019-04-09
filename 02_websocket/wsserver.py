
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import argparse
import time
from board import SCL, SDA
import busio 
from adafruit_neotrellis.neotrellis import NeoTrellis
import json

DEFAULT_PORT=8000
sockets = []
OFF = (0, 0, 0)
colors=[]

class NeoTrellisSocket(WebSocket):

    def handleMessage(self):
        
        try:
          data=json.loads(self.data)
          log(data["boardnumber"])
          log(data["number"])
          log((data["onKeyPressed"]))
          log((data["constant"]))
          
          if data["boardnumber"]==0 and data["number"]>=0 and data["number"]<16 and len(data["onKeyPressed"])==3 and len(data["constant"])==3:
            log("set entry for board {} led {}".format(data["boardnumber"],data["number"]))
            colors[data["number"]].setKeyPressedColor(data["onKeyPressed"][0],data["onKeyPressed"][1],data["onKeyPressed"][2])
            colors[data["number"]].setConstantColor(data["constant"][0],data["constant"][1],data["constant"][2])
            reconfigure()
          else:
            log("unknown message")
        except expression as identifier:
          log("error"+expression)
        # echo message back to client
        # self.sendMessage(self.data)

    def handleConnected(self):
        # print(self.address, 'connected')
        sockets.append(self)


    def handleClose(self):
        # print(self.address, 'closed')
        sockets.remove(self)


class KeyLedConfig:

  def __init__(self):
      self.onKeyPressed=OFF
      self.constant=OFF
  def setKeyPressedColor(self,r,g,b):
      self.onKeyPressed=(r,g,b)
      log("set keypressed color to ({},{},{})".format(r,g,b))
  def setConstantColor(self,r,g,b):
      log("set constant color to ({},{},{})".format(r,g,b))
      self.constant=(r,g,b)


class KeyEventCls:

  def __init__(self,event,number,boardnumber):
      if event==NeoTrellis.EDGE_RISING:
          self.event="keydown"
      elif event == NeoTrellis.EDGE_FALLING:
          self.event="keyup"
      else:
          self.event="unknown"
      self.number = number
      self.boardnumber = boardnumber


def broadCast(keyEvent):
    for socket in sockets:
        socket.sendMessage(json.dumps(keyEvent.__dict__))



def keyEvent(event):
  #turn the LED on when a rising edge is detected
  if event.edge == NeoTrellis.EDGE_RISING:
    trellis.pixels[event.number] = colors[event.number].onKeyPressed
  #turn the LED off when a rising edge is detected
  elif event.edge == NeoTrellis.EDGE_FALLING:
    trellis.pixels[event.number] = colors[event.number].constant
  broadCast(KeyEventCls(event.edge,event.number,0))


def reconfigure():
  for i in range(16):
    trellis.pixels[i] = colors[i].constant


def log(message):
  if(runAsDaemon==False):
    print(message)

runAsDaemon=False
port=DEFAULT_PORT
parser = argparse.ArgumentParser(description='websocketserver for NeoTrellis Keypad')
parser.add_argument('-p','--port',required=False, default=DEFAULT_PORT,
                   help='port for the websocket server')
parser.add_argument('-d', required=False,
                   help='run as daemon.no cli')

args = vars(parser.parse_args())
port=args["port"]


server = SimpleWebSocketServer('', port, NeoTrellisSocket)
#create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)
#create the trellis
trellis = NeoTrellis(i2c_bus)

for i in range(16):
  colors.append(KeyLedConfig())
  #activate rising edge events on all keys
  trellis.activate_key(i, NeoTrellis.EDGE_RISING)
  #activate falling edge events on all keys
  trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
  #set all keys to trigger the blink callback
  trellis.callbacks[i] = keyEvent

if runAsDaemon:
  while True:
    server.serveonce()
     #call the sync function call any triggered callbacks
    trellis.sync()
    #the trellis can only be read every 17 millisecons or so
    time.sleep(.02)

else:
  print("NeoTrellis KeyPad WebsocketServer")
  print("=================================")
  print("  Port: ",port)

  while True:
    server.serveonce()
     #call the sync function call any triggered callbacks
    trellis.sync()
    #the trellis can only be read every 17 millisecons or so
    time.sleep(.02)
  server.close()
