import network

from microdot import Microdot, Request, cors

ap_if: network.WLAN = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(
    essid='Pátečník',
    password='qwertyuiop',
    authmode=network.AUTH_WPA_WPA2_PSK
)

print(f'ip: {ap_if.ifconfig()[0]}')

app: Microdot = Microdot()
cors.CORS(app, '*')


@app.route('/', methods=['GET'])
async def index(request: Request):
    return '<h1>Hello World!</h1>', {'Content-Type': 'text/html'}


app.run(port=80)
