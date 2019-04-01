import utime
from HVACSys import HVACSys

MySys = HVACSys(12,27,14,33,21,39)
MySys.start()
while True:
    print(MySys.temp)
    print(MySys.humid)
    utime.sleep(2)
    if MySys.temp == 0:
        break
MySys.stop()
