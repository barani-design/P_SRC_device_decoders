#MeteoAg Iot Pro Gen2 periodic payload decoder ver.***
import sys

class parser:
    base = 16                                                                                                           #hexa base

    indexStart = 0                                                                                                      #starting position in payload
    indexLen   = 8                                                                                                      #length of variable in bits

    battStart  = 8
    battLen    = 1
    battRes    = 0.2
    battOffset = 3.3

    soilSelectorStart = 9
    soilSelectorLen = 3
    soilSelectorRes = 1

    tempSelectorStart = 12
    tempSelectorLen = 3
    tempSelectorRes = 1

    leafSelectorStart = 15
    leafSelectorLen = 3
    leafSelectorRes = 1

    E1Start = 18
    E1Len = 12
    E1Res = 1
    E1Offset = 0

    E2Start = 30
    E2Len = 12
    E2Res = 1
    E2Offset = 0

    E3Start = 42
    E3Len = 12
    E3Res = 1
    E3Offset = 0

    F1Start = 54
    F1Len = 12
    F1Res = 1
    F1Offset = 0

    F2Start = 66
    F2Len = 12
    F2Res = 1
    F2Offset = 0

    F3Start = 78
    F3Len = 12
    F3Res = 1
    F3Offset = 0

    G1Start = 90
    G1Len = 12
    G1Res = 1
    G1Offset = 0

    dbgStart = 102
    dbgLen = 2
    dbgRes = 1

    def __init__(self, inputString,numOfBytes ):                                                                        # internal storage for parsed variables
        self.battState = None
        self.batt = None

        self.soilSelector = None
        self.tempSelector = None
        self.LeafSelector = None

        self.E1 = None
        self.E2 = None
        self.E3 = None
        self.F1 = None
        self.F2 = None
        self.F3 = None
        self.G1 = None

        self.dbg = None
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

        self.soilSelector = int(''.join(self.binStringList[self.soilSelectorStart : self.soilSelectorStart + self.soilSelectorLen]),2)
        self.tempSelector = int(''.join(self.binStringList[self.tempSelectorStart : self.tempSelectorStart + self.tempSelectorLen]), 2)
        self.leafSelector = int(''.join(self.binStringList[self.leafSelectorStart : self.leafSelectorStart + self.leafSelectorLen]), 2)

        self.E1 = (int(''.join(self.binStringList[self.E1Start: self.E1Start + self.E1Len]), 2) * self.E1Res) + self.E1Offset
        self.E2 = (int(''.join(self.binStringList[self.E2Start: self.E2Start + self.E2Len]), 2) * self.E2Res) + self.E2Offset
        self.E3 = (int(''.join(self.binStringList[self.E3Start: self.E3Start + self.E3Len]), 2) * self.E3Res) + self.E3Offset

        self.F1 = (int(''.join(self.binStringList[self.F1Start: self.F1Start + self.F1Len]), 2) * self.F1Res) + self.F1Offset
        self.F2 = (int(''.join(self.binStringList[self.F2Start: self.F2Start + self.F2Len]), 2) * self.F2Res) + self.F2Offset
        self.F3 = (int(''.join(self.binStringList[self.F3Start: self.F3Start + self.F3Len]), 2) * self.F3Res) + self.F3Offset

        self.G1 = (int(''.join(self.binStringList[self.G1Start: self.G1Start + self.G1Len]), 2) * self.G1Res) + self.G1Offset

        self.dbg = int(''.join(self.binStringList[self.dbgStart: self.dbgStart + self.dbgLen]), 2)

        if enablePrint == 1:
            print("Index: " + str(self.index))

            if self.battState == 1:
                print("Batt: >" + str(format(self.batt, '.4f')) + "V")
            else:
                print("Batt: <" + str(format(self.batt, '.4f')) + "V")

            print("Soil selector: " + str(self.soilSelector))
            print("Temp selector: " + str(self.tempSelector))
            print("Leaf selector: " + str(self.leafSelector))

            print("==ADC RAW==")
            print("E1 : " + str(self.E1))
            print("E2 : " + str(self.E2))
            print("E3 : " + str(self.E3))

            print("F1 : " + str(self.F1))
            print("F2 : " + str(self.F2))
            print("F3 : " + str(self.F3))

            print("G1 : " + str(self.G1))

            if self.dbg == 1:
                print("DBG bits available")
            else:
                print("DBG: No error")

##### EXAMPLE CODE #####

print("MeteoAltim decoder example code")                                                                               # uncomment if you want to run it from IDE
d = parser("06B6C7D47E87E87F47EC7E87E4", 13)
d.parsePayload(1)

# if __name__ == "__main__":                                                                                              # uncomment if you want to run it from CMD line
#     print("MeteoAltim parser example code")
#     bytesToDecode = 16
#     d = parser(str(sys.argv[1]), bytesToDecode)
#     d.parsePayload(1)