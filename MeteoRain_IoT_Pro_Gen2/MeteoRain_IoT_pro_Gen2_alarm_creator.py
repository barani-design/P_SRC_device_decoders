#Meteo Rain Alarm creator ver.***
import sys

class creator:
    bitLenAlarmTime = 2
    bitLenTime      = 9
    bitLenInterval  = 10

    def __init__(self, alarmType, snoozeTime, timeInterval):
        self.snoozeTime = snoozeTime
        self.alarmType  = alarmType
        self.timeInterval = timeInterval
        self.alarmString = [0] * 32
    def createAlarm(self, enablePrint):                                                                                # if print 1 then print parsed payload
        self.snoozeTime = list(str(bin(int(str(int(self.snoozeTime/5))))[2:].zfill(self.bitLenTime)))
        self.alarmType = list(str(bin(int(str(int(self.alarmType))))[2:].zfill(self.bitLenAlarmTime)))
        self.timeInterval = list(str(bin(int(str(int(self.timeInterval))))[2:].zfill(self.bitLenInterval)))

        self.alarmString = self.alarmType + self.snoozeTime + self.timeInterval
        self.alarmString = hex(int(''.join(self.alarmString),2))[2:].zfill(8)

        if enablePrint == 1:
            print("Alarm payload: ",self.alarmString.upper())

##### EXAMPLE CODE #####

# print("MeteoRain Alarm creator example code")                                                                               # uncomment if you want to run it from IDE
# d = creator(0,600, 4)
# d.createAlarm(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoRain Alarm creator example code")
    d = creator(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
    d.createAlarm(1)