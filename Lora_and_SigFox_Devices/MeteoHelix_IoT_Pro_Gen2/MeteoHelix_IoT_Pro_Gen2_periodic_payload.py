#MeteoHelix IoT Pro Gen2 decoder ver.12.6.2025***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    indexStart = 0                                                                                                      #starting position in payload
    indexLen   = 8                                                                                                      #length of variable in bits

    battStart  = 8
    battLen    = 1
    battRes    = 0.2
    battOffset = 3.3

    tempStart  = 9
    tempLen    = 14
    tempRes    = 0.01                                                                                                   # if resolution is different than 1
    tempOffset = -50                                                                                                    # temp offset because this is minimal value

    tempMinStart = 23
    tempMinLen   = 8
    tempMinRes   = 0.05

    tempMaxStart = 31
    tempMaxLen   = 8
    tempMaxRes   = 0.05

    humStart   = 39
    humLen     = 9
    humRes     = 0.2

    pressBaseStart = 48                                                                                                 # starting position for pressures
    pressNum   = 1                                                                                                      # numbers of pressure sensor's
    pressLen   = 15
    pressRes   = 2.5
    pressOffset = 30000

    irraStart   = 63
    irraLen     = 11
    irraRes     = 1

    irraMinStart   = 74
    irraMinLen     = 10
    irraMinRes     = 2

    irraMaxStart   = 84
    irraMaxLen     = 10
    irraMaxRes     = 2

    rainClicksStart   = 94
    rainClicksLen     = 12
    rainClicksRes     = 1

    rainIntervalStart   = 106
    rainIntervalLen     = 10
    rainIntervalRes     = 1

    rainCorrectionStart   = 116
    rainCorrectionLen     = 10
    rainCorrectionRes     = 0.01

    heaterStart   = 126
    heaterLen     = 1
    
    alarmStart = 127
    alarmLen = 1

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.rainCorrection = None
        self.rainInterval = None
        self.rainClicks = None
        self.irraMax = None
        self.irraMin = None
        self.tempMax = None
        self.tempMin = None
        self.irra = None
        self.battState = None
        self.batt = None
        self.dbg = None
        self.press = [0] * self.pressNum
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
        self.battState = int(''.join(self.binStringList[self.battStart : self.battStart + self.battLen]),2)
        self.batt = ((self.index % 5) * self.battRes) + self.battOffset
        self.temp = (int(''.join(self.binStringList[self.tempStart: self.tempStart + self.tempLen]),2) * self.tempRes) + self.tempOffset
        self.tempMin = self.temp - (int(''.join(self.binStringList[self.tempMinStart: self.tempMinStart + self.tempMinLen]),2) * self.tempMinRes)
        self.tempMax = self.temp + (int(''.join(self.binStringList[self.tempMaxStart: self.tempMaxStart + self.tempMaxLen]),2) * self.tempMaxRes)
        self.hum = (int(''.join(self.binStringList[self.humStart: self.humStart + self.humLen]), 2) * self.humRes)

        for i in range(self.pressNum):
            self.press[i] = (int(int(''.join(self.binStringList[self.pressBaseStart + (self.pressLen * i) : self.pressBaseStart + (self.pressLen * i) + self.pressLen]),2)) * self.pressRes) + self.pressOffset

        self.irra = (int(''.join(self.binStringList[self.irraStart: self.irraStart + self.irraLen]), 2) * self.irraRes)
        self.irraMin = self.irra - (int(''.join(self.binStringList[self.irraMinStart: self.irraMinStart + self.irraMinLen]), 2) * self.irraMinRes)
        self.irraMax = self.irra + (int(''.join(self.binStringList[self.irraMaxStart: self.irraMaxStart + self.irraMaxLen]), 2) * self.irraMaxRes)
        self.rainClicks = (int(''.join(self.binStringList[self.rainClicksStart: self.rainClicksStart + self.rainClicksLen]), 2) * self.rainClicksRes)

        self.rainInterval = (int(''.join(self.binStringList[self.rainIntervalStart: self.rainIntervalStart + self.rainIntervalLen]), 2) * self.rainIntervalRes)
        if self.rainInterval != 0:
            self.rainInterval = (728/self.rainInterval)*(728/self.rainInterval)

        self.rainCorrection = (int(''.join(self.binStringList[self.rainCorrectionStart: self.rainCorrectionStart + self.rainCorrectionLen]), 2) * self.rainCorrectionRes)
        self.heater = int(''.join(self.binStringList[self.heaterStart: self.heaterStart + self.heaterLen]), 2)
        self.alarm = int(''.join(self.binStringList[self.alarmStart: self.alarmStart + self.alarmLen]), 2)

        # for i in range(self.pressNum):
        #     self.press[i] = int(int(''.join(self.binStringList[self.pressBaseStart + (self.pressLen * i) : self.pressBaseStart + (self.pressLen * i) + self.pressLen]),2) + self.pressOffset)

        if enablePrint == 1:
            print("Index: " + str(self.index))

            if self.battState == 1:
                print("Batt: !=" + str(format(self.batt, '.4f')) + "V")
            else:
                print("Batt: ==" + str(format(self.batt, '.4f')) + "V")

            print("Temp: " + str(format(self.temp, '.4f')) + "C")
            print("Temp MIN: " + str(format(self.tempMin, '.4f')) + "C")
            print("Temp MAX: " + str(format(self.tempMax, '.4f')) + "C")
            print("Hum: " + str(format(self.hum, '.4f')) + "%")

            for i in range(self.pressNum):
                print("Press_"+ str(i) +": "+ str(format(self.press[i], '.4f')) + "Pa")

            print("Irradiation: " + str(format(self.irra, '.4f')) + "W/m2")
            print("Irradiation MIN: " + str(format(self.irraMin, '.4f')) + "W/m2")
            print("Irradiation MAX: " + str(format(self.irraMax, '.4f')) + "W/m2")

            print("Rain clicks    : " + str(format(self.rainClicks, '.0f')))
            print("Rain interval  : " + str(format(self.rainInterval, '.3f')) + "s")
            print("Rain corrcetion: " + str(format(self.rainCorrection, '.2f')))
            print("Heater activated: " + str(format(self.heater, '')))
            print("Alarm sent: " + str(format(self.alarm, '')))
           

##### EXAMPLE CODE #####

# print("MeteoHelix decoder example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("93b44e0a06e6dd00020010040B0B0A00",16)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoHelix decoder example code")
    bytesToDecode = 16
    d = parser(str(sys.argv[1]), bytesToDecode)
    d.parsePayload(1)
