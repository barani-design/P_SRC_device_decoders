#Meteo Wind IoT SigFox 9B parser ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    typeStart  = 0                                                                                                      #starting position in payload
    typeLen    = 2                                                                                                      #length of variable in bits

    battStart   = 2
    battLen     = 5
    battRes     = 0.05
    battOffset  = 3

    windAveStart  = 7
    windAveLen    = 9
    windAveRes    = 0.1

    wind3sGustStart = 16
    wind3sGustLen = 9
    wind3sGustRes = 0.1

    wind3sMinStart = 25
    wind3sMinLen = 9
    wind3sMinRes = 0.1

    dirAveStart = 34
    dirAveLen = 9
    dirAveRes = 1

    dir3sGustStart = 43
    dir3sGustLen = 9
    dir3sGustRes = 1

    windVarHiStart = 52
    windVarHiLen  = 8
    windVarHiRes  = 1

    windVarLoStart  = 60
    windVarLoLen    = 8
    windVarLoRes    = 1

    dbgStart  = 68
    dbgLen    = 4
    dbgRes    = 1

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.type = None
        self.batt = None
        self.windAve = None
        self.wind3sGust = None
        self.wind3sMin = None
        self.dirAve = None
        self.dir3sGust = None
        self.VarHi = None
        self.VarLo = None

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
        self.windAve = (int(''.join(self.binStringList[self.windAveStart: self.windAveStart + self.windAveLen]), 2) * self.windAveRes)
        self.wind3sGust = self.windAve + (int(''.join(self.binStringList[self.wind3sGustStart: self.wind3sGustStart + self.wind3sGustLen]), 2) * self.wind3sGustRes)
        self.wind3sMin =  self.windAve - (int(''.join(self.binStringList[self.wind3sMinStart: self.wind3sMinStart + self.wind3sMinLen]), 2) * self.wind3sMinRes)
        self.dirAve = (int(''.join(self.binStringList[self.dirAveStart: self.dirAveStart + self.dirAveLen]), 2) * self.dirAveRes)
        self.dir3sGust  = (int(''.join(self.binStringList[self.dir3sGustStart: self.dir3sGustStart + self.dir3sGustLen]), 2) * self.dir3sGustRes)
    
        if enablePrint == 1:
            print("Type: " + str(self.type))
            print("Batt: " + str(format(self.batt, '.2f')) + "V")

            print("Wind_ave: " + str(format(self.windAve, '.2f')) + "m/s")
            print("Wind_3sgust: " + str(format(self.wind3sGust, '.2f')) + "m/s")
            print("Wind_3smin: " + str(format(self.wind3sMin, '.2f')) + "m/s")
            print("Dir_ave: " + str(format(self.dirAve, '.2f')) + "deg")
            print("Dir_3sgust: " + str(format(self.dir3sGust, '.2f')) + "deg")
          

            print("")
           

##### EXAMPLE CODE #####

# print("MeteoWind parser example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("c582a1087050904b3114",10)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoWind parser example code")
    bytesToDecode = 9
    d = parser(str(sys.argv[1]), bytesToDecode)
    d.parsePayload(1)