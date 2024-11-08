#Meteo Wind Alarm parser ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    indexStart = 0                                                                                                      #starting position in payload
    indexLen   = 6                                                                                                      #length of variable in bits

    hz3sGustStart = 6
    hz3sGustLen   = 11
    hz3sGustRes   = 0.1

    hz1sGustStart = 17
    hz1sGustLen   = 8
    hz1sGustRes   = 0.1

    deg1sGustStart = 25
    deg1sGustLen   = 9
    deg1sGustRes   = 1

    time1sGustStart = 34
    time1sGustLen   = 7
    time1sGustRes   = 5

    dbgStart   = 41
    dbgLen     = 7

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.hz3sGust = None
        self.hz1sGust = None
        self.deg1sGust = None
        self.time1sGust = None
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
        self.hz3sGust = (int(''.join(self.binStringList[self.hz3sGustStart: self.hz3sGustStart + self.hz3sGustLen]), 2) * self.hz3sGustRes)
        self.hz1sGust = self.hz3sGust + (int(''.join(self.binStringList[self.hz1sGustStart: self.hz1sGustStart + self.hz1sGustLen]), 2) * self.hz1sGustRes)
        self.deg1sGust = (int(''.join(self.binStringList[self.deg1sGustStart: self.deg1sGustStart + self.deg1sGustLen]), 2) * self.deg1sGustRes)
        self.time1sGust = (int(''.join(self.binStringList[self.time1sGustStart: self.time1sGustStart + self.time1sGustLen]), 2) * self.time1sGustRes)

        self.dbg = int(''.join(self.binStringList[self.dbgStart: self.dbgStart + self.dbgLen]), 2)

        if enablePrint == 1:
            print("Index: " + str(self.index))
            print("Hz_3s_gust: " + str(format(self.hz3sGust, '.4f')) + "Hz")
            print("Hz_1s_gust: " + str(format(self.hz1sGust, '.1f')) + "Hz")
            print("Deg_1s_gust: " + str(format(self.deg1sGust, '.1f')) + "Deg")
            print("Time_1s_gust: " + str(format(self.time1sGust, '.1f')) + "s")

            if self.dbg == 1:
                print("DBG:", self.dbg)
            else:
                print("DBG: No error")

##### EXAMPLE CODE #####

print("MeteoWind Alarm parser example code")                                                                               # uncomment if you want to run it from IDE
d = parser("18FA10E9B39180",6)
d.parsePayload(1)

# if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
#     print("MeteoWind Alarm parser example code")
#     bytesToDecode = 6
#     d = parser(str(sys.argv[1]), bytesToDecode)
#     d.parsePayload(1)