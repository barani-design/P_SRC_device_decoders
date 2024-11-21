#Meteo Rain Alarm parser ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    indexStart = 0                                                                                                      #starting position in payload
    indexLen   = 5                                                                                                      #length of variable in bits

    rainClicksStart = 5
    rainClicksLen   = 12
    rainClicksRes   = 1

    intervalTimeStart = 17
    intervalTimeLen   = 10
    intervalTimeRes   = 1

    dbgStart   = 27
    dbgLen     = 5

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.dbg = None
        self.intervalTime = None
        self.rainClicks = None
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
        self.rainClicks = (int(''.join(self.binStringList[self.rainClicksStart: self.rainClicksStart + self.rainClicksLen]), 2) * self.rainClicksRes)
        self.intervalTime = (int(''.join(self.binStringList[self.intervalTimeStart: self.intervalTimeStart + self.intervalTimeLen]), 2) * self.intervalTimeRes)

        self.dbg = int(''.join(self.binStringList[self.dbgStart: self.dbgStart + self.dbgLen]), 2)

        if enablePrint == 1:
            print("Index: " + str(self.index))
            print("Rain clicks: " + str(format(self.rainClicks, '.4f')) + "clicks")
            print("Time interval: " + str(format(self.intervalTime, '.4f')) + "s")

            if self.dbg == 1:
                print("DBG:", self.dbg)
            else:
                print("DBG: No error")

##### EXAMPLE CODE #####

print("MeteoRain Alarm parser example code")                                                                               # uncomment if you want to run it from IDE
d = parser("0A013240",4)
d.parsePayload(1)

# if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
#     print("MeteoRain Alarm parser example code")
#     bytesToDecode = 4
#     d = parser(str(sys.argv[1]), bytesToDecode)
#     d.parsePayload(1)