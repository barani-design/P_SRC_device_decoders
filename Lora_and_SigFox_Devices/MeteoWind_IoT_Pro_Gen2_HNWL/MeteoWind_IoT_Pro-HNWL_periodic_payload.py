#Meteo Wind-HNWL parser ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    indexStart  = 0                                                                                                      #starting position in payload
    indexLen    = 8                                                                                                      #length of variable in bits

    battStart   = 8
    battLen     = 2
    battRes     = 0.2
    battOffset  = 3.5

    windAvgBase = 10
    windAvgLen  = 10
    windAvgRes  = 0.1
    windAvgNum = 8

    dirAvgBase = 90
    dirAvgLen  = 8
    dirAvgRes  = 2
    dirAvgNum = 8

    dbgStart   = 154
    dbgLen     = 6

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.windAvg = [0.0] * self.windAvgNum
        self.dirAvg = [0.0] * self.dirAvgNum

        self.battState = None
        self.batt = None
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
        self.batt = ((self.battState * self.battRes) + self.battOffset)
        self.dbg = int(''.join(self.binStringList[self.dbgStart: self.dbgStart + self.dbgLen]), 2)

        for i in range(self.windAvgNum):
            self.windAvg[i] = float(int(''.join(self.binStringList[self.windAvgBase + (self.windAvgLen * i): self.windAvgBase + (self.windAvgLen * i) + self.windAvgLen]), 2) * self.windAvgRes)

        for i in range(self.dirAvgNum):
            self.dirAvg[i] = float(int(''.join(self.binStringList[self.dirAvgBase + (self.dirAvgLen * i): self.dirAvgBase + (self.dirAvgLen * i) + self.dirAvgLen]), 2) * self.dirAvgRes) 


        if enablePrint == 1:
            print("Index: " + str(self.index))

            if self.battState == 1:
                print("Batt: >" + str(format(self.batt, '.4f')) + "V")
            else:
                print("Batt: <" + str(format(self.batt, '.4f')) + "V")

            for i in range(self.windAvgNum):
                print("Wind_avg_"+ str(i) +": "+ str(format(self.windAvg[i], '.4f')) + "Hz")

            for i in range(self.dirAvgNum):
                print("Dir_avg"+ str(i) +": "+ str(format(self.dirAvg[i], '.0f')) + "deg")

            if self.dbg == 1:
                print("DBG: ",self.dbg)
            else:
                print("DBG: No error")

##### EXAMPLE CODE #####

# print("MeteoWind-HNWL parser example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("02C000000028E6012C080026AC83834B82814141",20)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoWind-HNWL parser example code")
    bytesToDecode = 20
    d = parser(str(sys.argv[1]), bytesToDecode)
    d.parsePayload(1)