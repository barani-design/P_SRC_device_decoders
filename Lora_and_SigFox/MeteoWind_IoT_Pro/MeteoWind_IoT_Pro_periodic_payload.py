#Meteo Wind parser ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    indexStart  = 0                                                                                                      #starting position in payload
    indexLen    = 8                                                                                                      #length of variable in bits

    battStart   = 8
    battLen     = 3
    battRes     = 0.2
    battOffset  = 3

    windAveStart  = 11
    windAveLen    = 9
    windAveRes    = 0.1

    wind3sGustStart = 20
    wind3sGustLen = 9
    wind3sGustRes = 0.1

    wind3sMinStart = 29
    wind3sMinLen = 9
    wind3sMinRes = 0.1

    windStdDevStart = 38
    windStdDevLen = 8
    windStdDevRes = 0.1

    dirAveStart = 46
    dirAveLen = 9
    dirAveRes = 1

    dir3sGustStart = 55
    dir3sGustLen = 9
    dir3sGustRes = 1

    dirStdDevStart = 64
    dirStdDevLen = 7
    dirStdDevRes = 1

    gustTime3sStart = 71
    gustTime3sLen  = 7
    gustTime3sRes  = 5

    vectorScalarStart  = 78
    vectorScalarLen    = 9
    vectorScalarRes    = 1

    alarmSentStart  = 79
    alarmSentLen    = 1
    alarmSentRes    = 1

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.windAve = None
        self.wind3sGust = None
        self.wind3sMin = None
        self.windStdDev = None
        self.dirAve = None
        self.dir3sGust = None
        self.dirStdDev = None
        self.gustTime3s = None
        self.vectorScalar = None
        self.alarmSent = None
        self.batt = None
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
        self.batt = (int(''.join(self.binStringList[self.battStart: self.battStart + self.battLen]),2) * self.battRes) + self.battOffset
        self.windAve = (int(''.join(self.binStringList[self.windAveStart: self.windAveStart + self.windAveLen]), 2) * self.windAveRes)
        self.wind3sGust = self.windAve + (int(''.join(self.binStringList[self.wind3sGustStart: self.wind3sGustStart + self.wind3sGustLen]), 2) * self.wind3sGustRes)
        self.wind3sMin =  self.windAve - (int(''.join(self.binStringList[self.wind3sMinStart: self.wind3sMinStart + self.wind3sMinLen]), 2) * self.wind3sMinRes)
        self.windStdDev  = (int(''.join(self.binStringList[self.windStdDevStart: self.windStdDevStart + self.windStdDevLen]), 2) * self.windStdDevRes)
        self.dirAve = (int(''.join(self.binStringList[self.dirAveStart: self.dirAveStart + self.dirAveLen]), 2) * self.dirAveRes)
        self.dir3sGust  = (int(''.join(self.binStringList[self.dir3sGustStart: self.dir3sGustStart + self.dir3sGustLen]), 2) * self.dir3sGustRes)
        self.dirStdDev = (int(''.join(self.binStringList[self.dirStdDevStart: self.dirStdDevStart + self.dirStdDevLen]), 2) * self.dirStdDevRes)
        self.gustTime3s = (int(''.join(self.binStringList[self.gustTime3sStart: self.gustTime3sStart + self.gustTime3sLen]), 2) * self.gustTime3sRes)
        self.vectorScalar = (int(''.join(self.binStringList[self.vectorScalarStart: self.vectorScalarStart + self.vectorScalarLen]), 2) * self.vectorScalarRes)
        self.alarmSent = (int(''.join(self.binStringList[self.alarmSentStart: self.alarmSentStart + self.alarmSentLen]), 2) * self.alarmSentRes)

        if enablePrint == 1:
            print("Index: " + str(self.index))
            print("Batt: " + str(format(self.batt, '.2f')) + "V")

            print("Wind_ave: " + str(format(self.windAve, '.2f')) + "m/s")
            print("Wind_3sgust: " + str(format(self.wind3sGust, '.2f')) + "m/s")
            print("Wind_3smin: " + str(format(self.wind3sMin, '.2f')) + "m/s")
            print("Wind_stdev: " + str(format(self.windStdDev, '.2f')) + "m/s")
            print("Dir_ave: " + str(format(self.dirAve, '.2f')) + "deg")
            print("Dir_3sgust: " + str(format(self.dir3sGust, '.2f')) + "deg")
            print("Dir_stdev: " + str(format(self.dirStdDev, '.2f')) + "deg")
            print("3sgust_time: " + str(format(self.gustTime3s)) + "sec")
            print("Vector/Scalar: " + str(format(self.vectorScalar)))
            print("Alarm sent?: " + str(format(self.alarmSent)))

            print("")
            if self.vectorScalar == 1:
                print("Measurement type -> Vector")
            else:
                print("Measurement type -> Scalar")

            if self.alarmSent == 1:
                print("Alarm sent!")
            else:
                print("Alarm did not occured")

##### EXAMPLE CODE #####

# print("MeteoWind parser example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("c582a1087050904b3114",10)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoWind parser example code")
    bytesToDecode = 10
    d = parser(str(sys.argv[1]), bytesToDecode)
    d.parsePayload(1)