def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('MBED', 'guni381!')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

try:
    do_connect()
except:
    do_connect()
