#Meteo Helix decoder ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    typeStart = 0                                                                                                      #starting position in payload
    typeLen   = 2                                                                                                      #length of variable in bits

    battStart  = 2
    battLen    = 5
    battRes    = 0.05
    battOffset = 3

    tempStart  = 7
    tempLen    = 11
    tempRes    = 0.1                                                                                                   # if resolution is different than 1
    tempOffset = -100                                                                                                    # temp offset because this is minimal value

    tempMinStart = 18
    tempMinLen   = 6
    tempMinRes   = 0.1

    tempMaxStart = 24
    tempMaxLen   = 6
    tempMaxRes   = 0.1

    humStart   = 30
    humLen     = 9
    humRes     = 0.2

    pressBaseStart = 39                                                                                                 # starting position for pressures
    pressNum   = 1                                                                                                      # numbers of pressure sensor's
    pressLen   = 14
    pressRes   = 5
    pressOffset = 50000

    irraStart   = 53
    irraLen     = 10
    irraRes     = 2

    irraMaxStart   = 63
    irraMaxLen     = 9
    irraMaxRes     = 2

    rainClicksStart   = 72
    rainClicksLen     = 8
    rainClicksRes     = 1

    rainIntervalStart   = 80
    rainIntervalLen     = 8
    rainIntervalRes     = 1


    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.rainInterval = None
        self.rainClicks = None
        self.irraMax = None
        self.tempMax = None
        self.tempMin = None
        self.irra = None
        self.battState = None
        self.batt = None
        self.press = [0] * self.pressNum
        self.hum = None
        self.temp = None
        self.type = None
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
        self.type = int(''.join(self.binStringList[self.typeStart : self.typeStart + self.typeLen]),2)
        self.batt = (int(''.join(self.binStringList[self.battStart: self.battStart + self.battLen]),2) * self.battRes) + self.battOffset
        self.temp = (int(''.join(self.binStringList[self.tempStart: self.tempStart + self.tempLen]),2) * self.tempRes) + self.tempOffset
        self.tempMin = (int(''.join(self.binStringList[self.tempMinStart: self.tempMinStart + self.tempMinLen]),2)* self.tempMinRes)
        self.tempMax = (int(''.join(self.binStringList[self.tempMaxStart: self.tempMaxStart + self.tempMaxLen]),2)* self.tempMaxRes)
        # self.tempMin = self.temp - (int(''.join(self.binStringList[self.tempMinStart: self.tempMinStart + self.tempMinLen]),2) * self.tempMinRes)
        # self.tempMax = self.temp + (int(''.join(self.binStringList[self.tempMaxStart: self.tempMaxStart + self.tempMaxLen]),2) * self.tempMaxRes)
        self.hum = (int(''.join(self.binStringList[self.humStart: self.humStart + self.humLen]), 2) * self.humRes)

        for i in range(self.pressNum):
            self.press[i] = (int(int(''.join(self.binStringList[self.pressBaseStart + (self.pressLen * i) : self.pressBaseStart + (self.pressLen * i) + self.pressLen]),2)) * self.pressRes) + self.pressOffset

        self.irra = (int(''.join(self.binStringList[self.irraStart: self.irraStart + self.irraLen]), 2) * self.irraRes)
        self.irraMax = (int(''.join(self.binStringList[self.irraMaxStart: self.irraMaxStart + self.irraMaxLen]), 2) * self.irraMaxRes)
        self.rainClicks = (int(''.join(self.binStringList[self.rainClicksStart: self.rainClicksStart + self.rainClicksLen]), 2) * self.rainClicksRes)

        self.rainInterval = (int(''.join(self.binStringList[self.rainIntervalStart: self.rainIntervalStart + self.rainIntervalLen]), 2) * self.rainIntervalRes)

        if enablePrint == 1:
            print("Type: " + str(self.type))

            print("Batt: " + str(format(self.batt, '.4f')) + "V")

            print("Temp: " + str(format(self.temp, '.4f')) + "C")
            print("Temp MIN: " + str(format(self.tempMin, '.4f')) + "C")
            print("Temp MAX: " + str(format(self.tempMax, '.4f')) + "C")
            print("Hum: " + str(format(self.hum, '.4f')) + "%")

            for i in range(self.pressNum):
                print("Press_"+ str(i) +": "+ str(format(self.press[i], '.4f')) + "Pa")

            print("Irradiation: " + str(format(self.irra, '.4f')) + "W/m2")
            print("Irradiation MAX: " + str(format(self.irraMax, '.4f')) + "W/m2")

            print("Rain clicks: " + str(format(self.rainClicks, '.0f')))
            print("Rain interval: " + str(format(self.rainInterval, '.3f')) + "s")

##### EXAMPLE CODE #####

# print("MeteoHelix decoder example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("712723674fa31afad303f0",11)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoHelix decoder example code")
    bytesToDecode = 11
    d = parser(str(sys.argv[1]), bytesToDecode)
    d.parsePayload(1)