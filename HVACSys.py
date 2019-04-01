import utime,dht,_thread,socket
from machine import Pin,ADC

class HVACSys:

    def __init__(self,StatePin1,StatePin2,LEDPin1,LEDPin2,DHTPin,ADCPin):
        self.S0 = Pin(StatePin1,Pin.OUT)
        self.S1 = Pin(StatePin2,Pin.OUT)
        self.LED0 = Pin(LEDPin1,Pin.OUT)
        self.LED1 = Pin(LEDPin2,Pin.OUT)
        self.CTRLmode = "OFF"
        self.HVACmode = "OFF"
        self.FANmode = "OFF"
        self.temp_setting = 65
        self.humid = 20
        self.temp = 65
        self.ADC_in = ADC(Pin(ADCPin))
        self.DHTSense = dht.DHT11(Pin(DHTPin))
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.workers = []
        self.stopFLG = False

        self.ADC_in.atten(ADC.ATTN_11DB)
        self.ADC_in.width(ADC.WIDTH_9BIT)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind(('192.168.43.154',5007))

    def networkWorker(self):
        while True:
            if self.stopFLG == True:
                break
            data,addr = self.sock.recvfrom(1024)
            data = data.decode('utf-8')
            print(data)
            if data == "MODE+ECO":
                print("ECO MODE")
                self.CTRLmode = "ECO"
            if "MODE+SET" in data:
                var,set,num = data.split("+")
                self.temp_setting = int(num)
                print("SET MODE")
                print("TEMP SETTING:" + str(self.temp_setting))
                self.CTRLmode = "SET"
            if data == "MODE+OFF":
                print("SYSTEM OFF")
                self.CTRLmode = "OFF"
            if data == "DISP":
                print(self.FANmode)
                print(self.HVACmode)
                print(self.CTRLmode)
                print(self.temp)
            if data == "TEMP+UP":
                self.temp_setting = self.temp_setting + 1
            if data == "TEMP+DOWN":
                self.temp_setting = self.temp_setting - 1
            if data == "HVAC+HEAT":
                self.HVACmode = "HEAT"
            if data == "HVAC+COOL":
                self.HVACmode = "COOL"
            if data == "SYSTEM+OFF":
                self.stopFLG = True
        return

    def tempWorker(self):
        while True:
            if self.stopFLG == True:
                break
            try:
                self.DHTSense.measure()
                self.temp = (self.DHTSense.temperature())*(9/5) + 32
                self.humid = self.DHTSense.humidity()
            except:
                self.temp = (self.ADC_in.read())*.27 + 40
                continue
            if self.CTRLmode == "ECO":
                if self.temp < 60:
                    self.HVACmode = "HEAT"
                    if self.temp > 57:
                        self.FANmode = "LOW"
                    elif self.temp > 55:
                        self.FANmode = "MED"
                    else:
                        self.FANmode = "HIGH"
                if self.temp > 75:
                    self.HVACmode = "COOL"
                    if self.temp < 77:
                        mod = "LOW"
                    elif self.temp < 80:
                        self.FANmode = "MED"
                    else:
                        self.FANmode = "HIGH"
                else:
                    self.FANmode = "OFF"
            if self.CTRLmode == "OFF":
                self.HVACmode = "OFF"
                self.FANmode = "OFF"
                continue
            if self.CTRLmode == "SET":
                if self.temp > self.temp_setting:
                    self.HVACmode = "COOL"
                    self.FANmode = "HIGH"
                if self.temp < self.temp_setting:
                    self.HVACmode = "HEAT"
                    self.FANmode = "HIGH"
                if self.temp == self.temp_setting:
                    self.HVACmode = "OFF"
                    self.FANmode = "OFF"
        return
    def controlWorker(self):
        while True:
            if self.FANmode == "LOW":
                self.S0.on()
                self.S1.off()
            if self.FANmode == "MED":
                self.S0.off()
                self.S1.on()
            if self.FANmode == "HIGH":
                self.S0.on()
                self.S1.on()
            if self.FANmode == "OFF":
                self.S0.off()
                self.S1.off()
            if self.HVACmode == "HEAT":
                self.LED0.on()
                self.LED1.off()
            if self.HVACmode == "COOL":
                self.LED0.off()
                self.LED1.on()
            if self.HVACmode == "OFF":
                self.LED0.off()
                self.LED1.off()
            if self.stopFLG == True:
                break
        return

    def start(self):
        print("Starting!")
        thread = _thread.start_new_thread(self.tempWorker,())
        self.workers.append(thread)
        thread = _thread.start_new_thread(self.controlWorker,())
        self.workers.append(thread)
        thread = _thread.start_new_thread(self.networkWorker,())
        self.workers.append(thread)

    def stop(self):
        self.stopFLG = True
        print("Exiting!")
