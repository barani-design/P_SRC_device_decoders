#Meteo Helix Alarm parser ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    indexStart = 0                                                                                                      #starting position in payload
    indexLen   = 5                                                                                                      #length of variable in bits

    alarmTypeStart = 5
    alarmTypeLen   = 3

    tempStart   = 8
    tempLen     = 11
    tempRes     = 0.05
    tempOffset  = -50

    humStart    = 19
    humLen      = 9
    humRes      = 0.2

    pressStart  = 28
    pressLen    = 15
    pressRes    = 3
    pressOffset = 30000

    irraStart   = 43
    irraLen     = 10
    irraRes     = 2

    rainClicksStart  = 53
    rainClicksLen    = 12
    rainClicksRes    = 1

    rainIntervalStart   = 65
    rainIntervalLen     = 10
    rainIntervalRes     = 1

    dbgStart   = 75
    dbgLen     = 4

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables

        self.irra = None
        self.rainClicks = None
        self.alarmType = None
        self.dbg = None
        self.press = None
        self.hum = None
        self.temp = None
        self.index = None
        self.binStringList = None
        self.inputString = inputString
        self.numOfBytes = numOfBytes

    def getBinString(self):                                                                                             # convert HEX string to binary string
        self.binString = bin(int(self.inputString, self.base))[2:].zfill(self.numOfBytes*8)
        return self.binString

    def getBinStringList(self):                                                                                         # convert HEX string to binary list
        self.binStringList = list(bin(int(self.inputString, self.base))[2:].zfill(self.numOfBytes*8))
        return self.binStringList

    def parseOneVariable(self, varStartPos, varLen, varOffset):                                                         # parse only one variable, you has to setup start position of first bit and variable length
        self.binStringList = list(bin(int(self.inputString, self.base))[2:].zfill(self.numOfBytes * 8))
        num = ''.join(self.binStringList[varStartPos:varStartPos+varLen])
        print("Parser variable", int(num, 2) + varOffset)

    def parsePayload(self, enablePrint):                                                                                # if print 1 then print parsed payload
        self.binStringList = list(bin(int(self.inputString, self.base))[2:].zfill(self.numOfBytes * 8))                 # parse payload string and convert it to variables
        self.index = int(''.join(self.binStringList[self.indexStart : self.indexStart + self.indexLen]),2)
        self.alarmType = int(''.join(self.binStringList[self.alarmTypeStart : self.alarmTypeStart + self.alarmTypeLen]),2)
        self.temp = (int(''.join(self.binStringList[self.tempStart: self.tempStart + self.tempLen]),2) * self.tempRes) + self.tempOffset
        self.hum = (int(''.join(self.binStringList[self.humStart: self.humStart + self.humLen]),2) * self.humRes)
        self.press = (int(''.join(self.binStringList[self.pressStart: self.pressStart + self.pressLen]), 2) * self.pressRes) + self.pressOffset
        self.irra = (int(''.join(self.binStringList[self.irraStart: self.irraStart + self.irraLen]),2) * self.irraRes)
        self.rainClicks = (int(''.join(self.binStringList[self.rainClicksStart: self.rainClicksStart + self.rainClicksLen]), 2) * self.rainClicksRes)

        self.rainInterval = (int(''.join(self.binStringList[self.rainIntervalStart: self.rainIntervalStart + self.rainIntervalLen]), 2) * self.rainIntervalRes)
        if self.rainInterval != 0:
            self.rainInterval = (728/self.rainInterval)*(728/self.rainInterval)

        self.dbg = int(''.join(self.binStringList[self.dbgStart: self.dbgStart + self.dbgLen]), 2)

        if enablePrint == 1:
            print("Index: " + str(self.index))

            if self.alarmType == 0:
                print("Alarm type - TEMPERATURE")
            elif self.alarmType == 1:
                print("Alarm type - HUMIDITY")
            elif self.alarmType == 2:
                print("Alarm type - PRESSURE")
            elif self.alarmType == 3:
                print("Alarm type - RAIN")

            print("Temperature current: " + str(format(self.temp, '.2f')) + "C")
            print("Humidity current: " + str(format(self.hum, '.1f')) + "%")
            print("Pressure current: " + str(format(self.press, '.1f')) + "Pa")
            print("Irradiation: " + str(format(self.irra, '.1f')) + "W/m2")
            print("Rain clicks: " + str(format(self.rainClicks, '.0f')))
            print("Rain interval: " + str(format(self.rainInterval, '.3f')) + "s")

            if self.dbg == 1:
                print("DBG:", self.dbg)
            else:
                print("DBG: No error")

##### EXAMPLE CODE #####

# print("MeteoHelix Alarm parser example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("00D098CB914040008360",10)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoHelix Alarm parser example code")
    bytesToDecode = 10
    d = parser(str(sys.argv[1]), bytesToDecode)
    d.parsePayload(1)