#Meteo Wind Alarm creator ver.***
import sys

class creator:
    bitLenTime  = 9
    bitLenUL    = 1
    bitLenUpper = 7
    bitLenLower = 7

    def __init__(self, snoozeTime, upperLower, lowTh, upTh):
        self.snoozeTime = snoozeTime
        self.upperLower = upperLower
        self.lowTh  = lowTh
        self.upTh   = upTh
        self.alarmString = [0] * 24
    def createAlarm(self, enablePrint):                                                                                # if print 1 then print parsed payload
        self.snoozeTime = list(str(bin(int(str(int(self.snoozeTime/5))))[2:].zfill(self.bitLenTime)))
        self.upperLower = list(str(bin(int(str(int(self.upperLower))))[2:].zfill(self.bitLenUL)))
        self.upTh = list(str(bin(int(str(int(self.upTh))))[2:].zfill(self.bitLenUpper)))
        self.lowTh = list(str(bin(int(str(int(self.lowTh))))[2:].zfill(self.bitLenLower)))

        self.alarmString = self.snoozeTime + self.upperLower + self.upTh + self.lowTh
        self.alarmString = hex(int(''.join(self.alarmString),2))[2:].zfill(6)

        if enablePrint == 1:
            print("Alarm payload: ",self.alarmString.upper())

##### EXAMPLE CODE #####

# print("MeteoWind Alarm creator example code")                                                                               # uncomment if you want to run it from IDE
# d = creator(120,1, 10, 10)
# d.createAlarm(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoWind Alarm creator example code")
    d = creator(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
    d.createAlarm(1)