#Meteo Helix Alarm creator ver.***
import sys

class creator:
    bitLenAlarmType = 2
    bitLenTime  = 9
    bitLenUL    = 2         #spolocny pre vsetky
    bitLenTemp  = 10
    bitLenHum   = 7
    bitLenPress = 13
    bitLenMinInterval = 10
    bitLenDebug = 9

    def __init__(self, alarmType, snoozeTime, tempUpperLower, lowTemp, upTemp, humUpperLower, lowHum, upHum, pressUpperLower, lowPress, upPress, minInterval, debug):
        self.alarmType = alarmType
        self.snoozeTime = snoozeTime

        self.tempUpperLower = tempUpperLower
        self.lowTemp  = lowTemp
        self.upTemp   = upTemp

        self.humUpperLower = humUpperLower
        self.lowHum = lowHum
        self.upHum = upHum

        self.pressUpperLower = pressUpperLower
        self.lowPress = lowPress
        self.upPress = upPress
        self.minInterval = minInterval
        self.debug = debug

        self.alarmString = [0] * 96


    def createAlarm(self, enablePrint):                                                                                # if print 1 then print parsed payload
        self.alarmType = list(str(bin(int(str(int(self.alarmType))))[2:].zfill(self.bitLenAlarmType)))
        self.snoozeTime = list(str(bin(int(str(int(self.snoozeTime/120))))[2:].zfill(self.bitLenTime)))

        self.tempUpperLower = list(str(bin(int(str(int(self.tempUpperLower))))[2:].zfill(self.bitLenUL)))               #
        self.lowTemp = list(str(bin(int(str(int(((self.lowTemp*10)+500)))))[2:].zfill(self.bitLenTemp)))                 #
        self.upTemp =  list(str(bin(int(str(int(((self.upTemp*10)+500)))))[2:].zfill(self.bitLenTemp)))                #

        self.humUpperLower = list(str(bin(int(str(int(self.humUpperLower))))[2:].zfill(self.bitLenUL)))                 #
        self.upHum = list(str(bin(int(str(int(self.upHum))))[2:].zfill(self.bitLenHum)))                                #
        self.lowHum = list(str(bin(int(str(int(self.lowHum))))[2:].zfill(self.bitLenHum)))                              #

        self.pressUpperLower = list(str(bin(int(str(int(self.pressUpperLower))))[2:].zfill(self.bitLenUL)))             #
        self.upPress =  list(str(bin(int(str(int(((self.upPress/ 10)-3000)))))[2:].zfill(self.bitLenPress)))
        self.lowPress = list(str(bin(int(str(int(((self.lowPress/10)-3000)))))[2:].zfill(self.bitLenPress)))

        self.minInterval = list(str(bin(int(str(int(self.minInterval))))[2:].zfill(self.bitLenMinInterval)))
        self.debug = list(str(bin(int(str(int(self.debug))))[2:].zfill(self.bitLenDebug)))

        self.alarmString = self.alarmType + self.snoozeTime + self.tempUpperLower + self.lowTemp + self.upTemp + self.humUpperLower + self.lowHum + self.upHum + self.pressUpperLower + self.lowPress + self.upPress + self.minInterval + self.debug
        self.alarmString = hex(int(''.join(self.alarmString),2))[2:].zfill(9)

        if enablePrint == 1:
            print("Alarm payload: ",self.alarmString)

##### EXAMPLE CODE #####
#
# print("MeteoWind Alarm creator example code")                                                                               # uncomment if you want to run it from IDE
# d = creator(3, 120,0, -16.4, 2.8, 3, 66, 85, 1, 57300, 84610, 298, 256)
# d.createAlarm(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoWind Alarm creator example code")
    d = creator(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9]), int(sys.argv[10]), int(sys.argv[11]), int(sys.argv[12]), int(sys.argv[13]))
    d.createAlarm(1)