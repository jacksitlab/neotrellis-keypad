# NeoTrellis 4x4 RGB LED Keypad Examples for Raspberry Pi

Manual: 
https://cdn-learn.adafruit.com/downloads/pdf/adafruit-neotrellis.pdf

All my examples are tested with a Pi Zero W with Raspbian Stretch(9.4). SDA and SCL on I2C1 (PIN3 + PIN5) and INT on GPIO4(PIN7).
Running with python 3.

## Prerequisites

 * sudo apt-get install python3-pip
 * sudo pip3 install adafruit-circuitpython-neotrellis

## 01_test

A simple test application to see if the board is running as expected

## 02_websocket

A websocket server which gives all keypressed events to a websocket client. With this you are able to connect your keypad to a web interface.
based on https://github.com/dpallot/simple-websocket-server

```
pip3 install SimpleWebSocketServer
```


KeyEventData:
```
[{
    "boardnumber":0,
    "event":"keydown" | "keyup",
    "number":0
}]
```
KeyLedConfig:
```
{
    boardnumber:0,
    number:0,
    onKeyPressed:[255,255,255],
    constant:[0,0,0]
}
```

index.html is an example how to use and set the keypad.
I cleaned the [farbtastic.js](https://github.com/mattfarina/farbtastic) lib from old compatibility code for IE so that it works with actual jquery.

## License

MIT