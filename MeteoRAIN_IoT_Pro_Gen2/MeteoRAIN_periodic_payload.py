#Meteo Rain decoder ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    indexStart = 0                                                                                                      #starting position in payload
    indexLen   = 8                                                                                                      #length of variable in bits

    battStart  = 8
    battLen    = 1
    battRes    = 0.2
    battOffset = 3.3

    rainClicksStart   = 9
    rainClicksLen     = 12
    rainClicksRes     = 1

    rainIntervalStart   = 21
    rainIntervalLen     = 10
    rainIntervalRes     = 1

    rainCorrectionStart   = 31
    rainCorrectionLen     = 12
    rainCorrectionRes     = 0.01

    isTempStart = 43
    isTempLen   = 1

    dbgStart   = 44
    dbgLen     = 4

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.rainCorrection = None
        self.rainInterval = None
        self.rainClicks = None
        self.battState = None
        self.batt = None
        self.isTemp = None
        self.dbg = None
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
        self.rainClicks = (int(''.join(self.binStringList[self.rainClicksStart: self.rainClicksStart + self.rainClicksLen]), 2) * self.rainClicksRes)

        self.rainInterval = (int(''.join(self.binStringList[self.rainIntervalStart: self.rainIntervalStart + self.rainIntervalLen]), 2) * self.rainIntervalRes)
        if self.rainInterval != 0:
            self.rainInterval = (728/self.rainInterval)*(728/self.rainInterval)

        self.rainCorrection = (int(''.join(self.binStringList[self.rainCorrectionStart: self.rainCorrectionStart + self.rainCorrectionLen]), 2) * self.rainCorrectionRes)
        self.isTemp = int(''.join(self.binStringList[self.isTempStart: self.isTempStart + self.isTempLen]), 2)
        self.dbg = int(''.join(self.binStringList[self.dbgStart: self.dbgStart + self.dbgLen]), 2)

        # for i in range(self.pressNum):
        #     self.press[i] = int(int(''.join(self.binStringList[self.pressBaseStart + (self.pressLen * i) : self.pressBaseStart + (self.pressLen * i) + self.pressLen]),2) + self.pressOffset)

        if enablePrint == 1:
            print("Index: " + str(self.index))

            if self.battState == 1:
                print("Batt: >" + str(format(self.batt, '.4f')) + "V")
            else:
                print("Batt: <" + str(format(self.batt, '.4f')) + "V")

            print("Rain clicks: " + str(format(self.rainClicks, '.0f')))
            print("Rain interval: " + str(format(self.rainInterval, '.3f')) + "s")
            print("Rain corrcetion: " + str(format(self.rainCorrection, '.2f')))

            if self.isTemp == 1:
                print("Temperature is above 2C")
            else:
                print("Temperature is below 2C")

            if self.dbg == 1:
                print("DBG: Pressure sensor error!")
            else:
                print("DBG: No error")

##### EXAMPLE CODE #####

print("MeteoRain decoder example code")                                                                               # uncomment if you want to run it from IDE
d = parser("0b8013240051",6)
d.parsePayload(1)

# if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
#     print("MeteoRain decoder example code")
#     bytesToDecode = 6
#     d = parser(str(sys.argv[1]), bytesToDecode)
#     d.parsePayload(1)