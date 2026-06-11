#Meteo Wind parser ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    indexStart  = 0                                                                                                      #starting position in payload
    indexLen    = 8                                                                                                      #length of variable in bits

    battStart   = 8
    battLen     = 1
    battRes     = 0.2
    battOffset  = 3.3

    windAveStart  = 9
    windAveLen    = 12
    windAveRes    = 0.02

    wind3sGustStart = 21
    wind3sGustLen = 9
    wind3sGustRes = 0.1

    wind1sGustStart = 30
    wind1sGustLen = 8
    wind1sGustRes = 0.1

    wind3sMinStart = 38
    wind3sMinLen = 9
    wind3sMinRes = 0.1

    windStdDevStart = 47
    windStdDevLen = 8
    windStdDevRes = 0.1

    dirAveStart = 55
    dirAveLen = 9
    dirAveRes = 1

    dir1sGustStart = 64
    dir1sGustLen = 9
    dir1sGustRes = 1

    dirStdDevStart = 73
    dirStdDevLen = 8
    dirStdDevRes = 1

    gustTime1sStart = 81
    gustTime1sLen  = 7
    gustTime1sRes  = 5

    alarmSentStart  = 88
    alarmSentLen    = 1
    alarmSentRes    = 1

    debugFlagsStart  = 89
    debugFlagsLen    = 7

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.windAve = None
        self.wind3sGust = None
        self.wind1sGust = None
        self.wind3sMin = None
        self.windStdDev = None
        self.dirAve = None
        self.dir1sGust = None
        self.dirStdDev = None
        self.gustTime1s = None
        self.alarmSent = None
        self.debugFlags = None
        self.batt = None
        self.battState = None
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
        self.battState = int(''.join(self.binStringList[self.battStart: self.battStart + self.battLen]),2)               # 1 = exact value, 0 = approximate value
        self.batt = ((self.index % 5) * self.battRes) + self.battOffset                                                 # V_bat derived from Index: =IF(MOD(Index,10)<=4, MOD(Index,10)*battRes+battOffset, ...-1)
        self.windAve = (int(''.join(self.binStringList[self.windAveStart: self.windAveStart + self.windAveLen]), 2) * self.windAveRes)
        self.wind3sGust = self.windAve + (int(''.join(self.binStringList[self.wind3sGustStart: self.wind3sGustStart + self.wind3sGustLen]), 2) * self.wind3sGustRes)
        self.wind1sGust = self.wind3sGust + (int(''.join(self.binStringList[self.wind1sGustStart: self.wind1sGustStart + self.wind1sGustLen]), 2) * self.wind1sGustRes)
        self.wind3sMin =  (int(''.join(self.binStringList[self.wind3sMinStart: self.wind3sMinStart + self.wind3sMinLen]), 2) * self.wind3sMinRes)
        self.windStdDev  = (int(''.join(self.binStringList[self.windStdDevStart: self.windStdDevStart + self.windStdDevLen]), 2) * self.windStdDevRes)
        self.dirAve = (int(''.join(self.binStringList[self.dirAveStart: self.dirAveStart + self.dirAveLen]), 2) * self.dirAveRes)
        self.dir1sGust  = (int(''.join(self.binStringList[self.dir1sGustStart: self.dir1sGustStart + self.dir1sGustLen]), 2) * self.dir1sGustRes)
        self.dirStdDev = (int(''.join(self.binStringList[self.dirStdDevStart: self.dirStdDevStart + self.dirStdDevLen]), 2) * self.dirStdDevRes)
        self.gustTime1s = (int(''.join(self.binStringList[self.gustTime1sStart: self.gustTime1sStart + self.gustTime1sLen]), 2) * self.gustTime1sRes)
        self.alarmSent = (int(''.join(self.binStringList[self.alarmSentStart: self.alarmSentStart + self.alarmSentLen]), 2) * self.alarmSentRes)
        self.debugFlags = int(''.join(self.binStringList[self.debugFlagsStart: self.debugFlagsStart + self.debugFlagsLen]), 2)

        if enablePrint == 1:
            print("Index: " + str(self.index))
            if self.battState == 1:
                print("Batt: == " + str(format(self.batt, '.1f')) + "V")
            else:
                print("Batt: != " + str(format(self.batt, '.1f')) + "V")

            print("Hz_avg: " + str(format(self.windAve, '.2f')) + "Hz")
            print("Hz_3s_gust: " + str(format(self.wind3sGust, '.2f')) + "Hz")
            print("Hz_1s_gust: " + str(format(self.wind1sGust, '.2f')) + "Hz")
            print("Hz_3s_min: " + str(format(self.wind3sMin, '.2f')) + "Hz")
            print("Hz_1s_stdev: " + str(format(self.windStdDev, '.2f')) + "Hz")
            print("Deg_1s_avg: " + str(format(self.dirAve, '.2f')) + "deg")
            print("Deg_1s_gust: " + str(format(self.dir1sGust, '.2f')) + "deg")
            print("Deg_1s_stdev: " + str(format(self.dirStdDev, '.2f')) + "deg")
            print("Time_1s_gust: " + str(format(self.gustTime1s)) + "sec")
            print("Alarm sent?: " + str(format(self.alarmSent)))
            print("Debug flags: " + str(format(self.debugFlags)))

            print("")
            if self.alarmSent == 1:
                print("Alarm sent!")
            else:
                print("Alarm did not occured")

##### EXAMPLE CODE #####

# print("MeteoWind parser example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("1981205C00000ECF59FF8F01",12)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoWind parser example code")
    bytesToDecode = 12
    d = parser(str(sys.argv[1]), bytesToDecode)
    d.parsePayload(1)
