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

    hzAvgStart  = 9
    hzAvgLen    = 12
    hzAvgRes    = 0.02

    hz3sGustStart = 21
    hz3sGustLen = 9
    hz3sGustRes = 0.1

    hz1sGustStart = 30
    hz1sGustLen = 8
    hz1sGustRes = 0.1

    hz3sMinStart = 38
    hz3sMinLen = 9
    hz3sMinRes = 0.1

    hz1sStdDevStart = 47
    hz1sStdDevLen = 8
    hz1sStdDevRes = 0.1

    deg1sAvgStart = 55
    deg1sAvgLen = 9
    deg1sAvgRes = 1

    deg1sGustStart = 64
    deg1sGustLen = 9
    deg1sGustRes = 1

    deg1sStdDevStart = 73
    deg1sStdDevLen  = 8
    deg1sStdDevRes  = 1

    degCcwMinStart  = 81
    degCcwMinLen    = 9
    degCcwMinRes    = 1

    degCwMaxStart  = 90
    degCwMaxLen    = 9
    degCwMaxRes    = 1

    time1sGustStart = 99
    time1sGustLen   = 7
    time1sGustRes   = 1

    alarmSentStart  = 106
    alarmSentLen    = 1

    dbgStart   = 107
    dbgLen     = 1

    def __init__(self, inputString, numOfBytes):                                                                        # internal storage for parsed variables
        self.hz3sMin = None
        self.hz1StdDev = None
        self.deg1sAvg = None
        self.deg1sGust = None
        self.deg1sStdDev = None
        self.degCwMax = None
        self.degCcwMin = None
        self.time1sGust = None
        self.alarmSent = None
        self.hz1sGust = None
        self.hz3sGust = None
        self.hzAvg = None
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
        self.batt = ((self.index % 5) * self.battRes) + self.battOffset
        self.hzAvg = (int(''.join(self.binStringList[self.hzAvgStart: self.hzAvgStart + self.hzAvgLen]), 2) * self.hzAvgRes)
        self.hz3sGust = self.hzAvg + (int(''.join(self.binStringList[self.hz3sGustStart: self.hz3sGustStart + self.hz3sGustLen]), 2) * self.hz3sGustRes)
        self.hz1sGust =  self.hz3sGust + (int(''.join(self.binStringList[self.hz1sGustStart: self.hz1sGustStart + self.hz1sGustLen]), 2) * self.hz1sGustRes)
        self.hz3sMin  = (int(''.join(self.binStringList[self.hz3sMinStart: self.hz3sMinStart + self.hz3sMinLen]), 2) * self.hz3sMinRes)
        self.hz1StdDev = (int(''.join(self.binStringList[self.hz1sStdDevStart: self.hz1sStdDevStart + self.hz1sStdDevLen]), 2) * self.hz1sStdDevRes)
        self.deg1sAvg  = (int(''.join(self.binStringList[self.deg1sAvgStart: self.deg1sAvgStart + self.deg1sAvgLen]), 2) * self.deg1sAvgRes)
        self.deg1sGust = (int(''.join(self.binStringList[self.deg1sGustStart: self.deg1sGustStart + self.deg1sGustLen]), 2) * self.deg1sGustRes)
        self.deg1sStdDev = (int(''.join(self.binStringList[self.deg1sStdDevStart: self.deg1sStdDevStart + self.deg1sStdDevLen]), 2) * self.deg1sStdDevRes)
        self.degCcwMin = (int(''.join(self.binStringList[self.degCcwMinStart: self.degCcwMinStart + self.degCcwMinLen]), 2) * self.degCcwMinRes)
        self.degCwMax = (int(''.join(self.binStringList[self.degCwMaxStart: self.degCwMaxStart + self.degCwMaxLen]), 2) * self.degCwMaxRes)
        self.time1sGust = (int(''.join(self.binStringList[self.time1sGustStart: self.time1sGustStart + self.time1sGustLen]), 2) * self.time1sGustRes)
        self.alarmSent = int(''.join(self.binStringList[self.alarmSentStart: self.alarmSentStart + self.alarmSentLen]), 2)
        self.dbg = int(''.join(self.binStringList[self.dbgStart: self.dbgStart + self.dbgLen]), 2)

        if enablePrint == 1:
            print("Index: " + str(self.index))

            if self.battState == 1:
                print("Batt: >" + str(format(self.batt, '.4f')) + "V")
            else:
                print("Batt: <" + str(format(self.batt, '.4f')) + "V")

            print("Hz_avg: " + str(format(self.hzAvg, '.4f')) + "Hz")
            print("Hz_3s_gust: " + str(format(self.hz3sGust, '.4f')) + "Hz")
            print("Hz_1s_gust: " + str(format(self.hz1sGust, '.4f')) + "Hz")
            print("Hz_3s_min: " + str(format(self.hz3sMin, '.4f')) + "Hz")
            print("Hz_1s_stdev: " + str(format(self.hz1StdDev, '.4f')) + "Hz")
            print("Deg_1s_avg: " + str(format(self.deg1sAvg, '.4f')) + "deg")
            print("Deg_1s_gust: " + str(format(self.deg1sGust, '.4f')) + "deg")
            print("Deg_1s_stdev: " + str(format(self.deg1sStdDev, '.4f')) + "deg")
            print("Deg_ccw_min: " + str(format(self.degCcwMin, '.4f')) + "deg")
            print("Deg_cw_max: " + str(format(self.degCwMax, '.4f')) + "deg")
            print("Time_1s_gust: " + str(format(self.time1sGust, '.4f')) + "deg")

            if self.alarmSent == 1:
                print("Alarm sent!")
            else:
                print("Alarm did not occured")

            if self.dbg == 1:
                print("DBG: Pressure sensor error!")
            else:
                print("DBG: No error")

##### EXAMPLE CODE #####

# print("MeteoWind parser example code")                                                                               # uncomment if you want to run it from IDE
# d = parser("9f03e8080c2e0a00b4005a2d0000",14)
# d.parsePayload(1)

if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
    print("MeteoWind parser example code")
    bytesToDecode = 14
    d = parser(str(sys.argv[1]), bytesToDecode)
    d.parsePayload(1)