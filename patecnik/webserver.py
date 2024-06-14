import network
from microdot import Microdot, Request
from microdot.cors import CORS
from microdot.websocket import with_websocket, WebSocket

import constants

print('Setting up WIFI...')
ap_if: network.WLAN = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(
    essid=constants.ESSID,
    password=constants.PASSWORD,
    authmode=network.AUTH_WPA_WPA2_PSK
)

ifconfig: tuple[str, str, str, str] = (constants.IP, '255.255.255.0', constants.IP, '8.8.8.8')
ap_if.ifconfig(ifconfig)

print('WIFI set up successfully\n')
print(f'ESSID: {constants.ESSID}')
print(f'Password: {constants.PASSWORD}')
print(f'IP: {ap_if.ifconfig()[0]}\n')

app: Microdot = Microdot()
CORS(app, '*')


@app.route('/')
@with_websocket
async def index(request: Request, websocket: WebSocket):
    while True:
        message = await websocket.receive()
        print(message)
        await websocket.send('juuu dostal jsem: ' + message)


app.run(port=80)
