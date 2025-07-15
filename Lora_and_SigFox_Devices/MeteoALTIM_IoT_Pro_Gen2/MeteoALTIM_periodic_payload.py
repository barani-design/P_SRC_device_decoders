#Meteo Altim decoder ver.***
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
    tempLen    = 6
    tempRes    = 2                                                                                                   # if resolution is different than 1
    tempOffset = -45                                                                                                    # temp offset because this is minimal value

    humStart   = 15
    humLen     = 4
    humRes     = 4
    humOffset  = 40

    refPressStart = 19
    refPressLen = 13
    refPressRes = 10
    refPressOffset = 30000

    pressCount = 6

    diffPressStart = 32
    diffPressLen = 10
    diffPressRes = 0.5
    diffPressOffset = -256

    stdDevStart = 92
    stdDevLen = 6
    stdDevRes = 1


    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.battState = None
        self.batt = None
        self.dbg = None
        self.refPress = None
        self.hum = None
        self.temp = None
        self.index = None
        self.binStringList = None
        self.inputString = inputString
        self.numOfBytes = numOfBytes
        self.diffPress = [0] * self.pressCount
        self.stdDev = [0] * self.pressCount
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
        self.temp = (int(''.join(self.binStringList[self.tempStart: self.tempStart + self.tempLen]), 2) * self.tempRes) + self.tempOffset
        self.hum =  (int(''.join(self.binStringList[self.humStart : self.humStart + self.humLen]),2) * self.humRes) + self.humOffset
        self.refPress = int(''.join(self.binStringList[self.refPressStart : self.refPressStart + self.refPressLen]),2)

        for i in range(self.pressCount):
            self.diffPress[i] = (int(''.join(self.binStringList[self.diffPressStart + (self.diffPressLen * i) : self.diffPressStart + (self.diffPressLen * i) + self.diffPressLen]),2) * self.diffPressRes) + self.diffPressOffset

        for i in range(self.pressCount):
            self.stdDev[i] = int(''.join(self.binStringList[self.stdDevStart + (self.stdDevLen * i) : self.stdDevStart + (self.stdDevLen * i) + self.stdDevLen]),2)

        if enablePrint == 1:
            print("Index: " + str(self.index))

            if self.battState == 1:
                print("Batt: >" + str(format(self.batt, '.4f')) + "V")
            else:
                print("Batt: <" + str(format(self.batt, '.4f')) + "V")

            print("Temp: " + str(self.temp) + "C")
            print("Hum: " + str(self.hum) + "%")

            for i in range(self.pressCount):
                print("diffPress"+ str(i) +": "+ str(format(self.diffPress[i], '.1f')) + "Pa")

            for i in range(self.pressCount):
                print("stdDev"+ str(i) +": "+ str(format(self.stdDev[i], '.1f')) + "Pa")

            if self.dbg == 1:
                print("DBG: Pressure sensor error!")
            else:
                print("DBG: No error")

##### EXAMPLE CODE #####

# print("MeteoAltim decoder example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("your payload to decode",16)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoAltim parser example code")
    bytesToDecode = 16
    d = parser(str(sys.argv[1]), bytesToDecode)
    d.parsePayload(1)