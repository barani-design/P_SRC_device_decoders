#Meteo Altim parser ver.***
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
    tempLen    = 9
    tempRes    = 0.25                                                                                                   # if resolution is different than 1
    tempOffset = -50                                                                                                    # temp offset because this is minimal value

    humStart   = 18
    humLen     = 7

    pressBaseStart = 25                                                                                                 # starting position for pressures
    pressNum   = 6                                                                                                      # numbers of pressure sensor's
    pressLen   = 17
    pressOffset = 30000

    dbgStart   = 127
    dbgLen     = 1

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
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
        self.temp = (int(''.join(self.binStringList[self.tempStart: self.tempStart + self.tempLen]), 2) * self.tempRes) + self.tempOffset
        self.hum = int(''.join(self.binStringList[self.humStart : self.humStart + self.humLen]),2)
        self.dbg = int(''.join(self.binStringList[self.dbgStart: self.dbgStart + self.dbgLen]), 2)

        for i in range(self.pressNum):
            self.press[i] = int(int(''.join(self.binStringList[self.pressBaseStart + (self.pressLen * i) : self.pressBaseStart + (self.pressLen * i) + self.pressLen]),2) + self.pressOffset)

        if enablePrint == 1:
            print("Index: " + str(self.index))

            if self.battState == 1:
                print("Batt: >" + str(format(self.batt, '.4f')) + "V")
            else:
                print("Batt: <" + str(format(self.batt, '.4f')) + "V")

            print("Temp: " + str(self.temp) + "C")
            print("Hum: " + str(self.hum) + "%")

            for i in range(self.pressNum):
                print("Press_"+ str(i) +": "+ str(self.press[i]) + "Pa")

            if self.dbg == 1:
                print("DBG: Pressure sensor error!", self.dbg)
            else:
                print("DBG: No error")

##### EXAMPLE CODE #####

# print("MeteoAltim parser example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("your payload to decode",16)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoAltim parser example code")
    d = parser(str(sys.argv[1]),int(sys.argv[2]))
    d.parsePayload(1)