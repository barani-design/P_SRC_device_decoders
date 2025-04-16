#Meteo Rain Alarm creator ver.***
import sys
import math
class creator:
    bitLenAlarmType = 2
    bitLenTime      = 9
    bitLenInterval  = 10
    bitLenDebug =  11

    def __init__(self, alarmType, snoozeTime, timeInterval, debug):
        self.snoozeTime = snoozeTime
        self.alarmType  = alarmType
        self.timeInterval = timeInterval
        self.debug = debug
        self.alarmString = [0] * 32
    def createAlarm(self, enablePrint):                                                                                # if print 1 then print parsed payload
        self.alarmType = list(str(bin(int(str(int(self.alarmType))))[2:].zfill(self.bitLenAlarmType)))
        self.snoozeTime = list(str(bin(int(str(int(self.snoozeTime/120))))[2:].zfill(self.bitLenTime)))
        self.timeInterval = 728 / math.sqrt(self.timeInterval)
        self.timeInterval = list(str(bin(int(str(int(self.timeInterval))))[2:].zfill(self.bitLenInterval)))
        self.debug = list(str(bin(int(str(int(self.debug))))[2:].zfill(self.bitLenDebug)))

        self.alarmString = self.alarmType + self.snoozeTime + self.timeInterval + self.debug
        self.alarmString = hex(int(''.join(self.alarmString),2))

        if enablePrint == 1:
            value = int(self.alarmString.replace("0x", ""), 16)
            print(f"Alarm payload: {value:08x}")

##### EXAMPLE CODE #####

print("MeteoRain Alarm creator example code")                                                                               # uncomment if you want to run it from IDE
d = creator(0,600, 10, 0)
d.createAlarm(1)

#alarmType(0-3) snoozeTime in sec(0-61440 multiply of 120) minInterval(0-1023) debug(0-2048)
# python MeteoRain_IoT_pro_Gen2_alarm_creator.py 0 600 4 1
# if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
#     print("MeteoRain Alarm creator example code")
#     d = creator(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]), int(sys.argv[4]))
#     d.createAlarm(1)