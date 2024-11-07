## Ahoj ja som skrypt. Ked mi das na vstupl platny payload, vyplujem ti dekodovane data
## data budu pekne v poradi ako su v exceli, float na 4 desatinne,
## zarovnane tabelatormi..              #Seva kamo, bardzo fajny skrypt sa nakodzi

class decoder:
    base = 16                                      #hexa base

    indexStart = 0                                 #starting position in payload
    indexLen   = 8                                 #length of variable in bits

    battStart  = 8
    battLen    = 1

    tempStart  = 9
    tempLen    = 9
    tempRes    = 0.25                              # if resolution is different than 1
    tempOffset = -50                               # temp offset because this is minimal value

    humStart   = 18
    humLen     = 7

    pressBaseStart = 25                            # starting position for pressures
    pressNum   = 6                                 # numbers of pressure sensor's
    pressLen   = 17
    pressOffset = 30000

    dbgStart   = 127
    dbgLen     = 1

    def __init__(self, inputString, numOfBytes):
        self.dbg = None
        self.press = [0] * self.pressNum
        self.hum = None
        self.temp = None
        self.index = None
        self.binStringList = None
        self.inputString = inputString
        self.numOfBytes = numOfBytes

    def getBinString(self):
        self.binString = bin(int(self.inputString, self.base))[2:].zfill(self.numOfBytes*8)
        return self.binString

    def getBinStringList(self):
        self.binStringList = list(bin(int(self.inputString, self.base))[2:].zfill(self.numOfBytes*8))
        return self.binStringList

    def parseOneVariable(self, varStartPos, varLen, varOffset):
        self.binStringList = list(bin(int(self.inputString, self.base))[2:].zfill(self.numOfBytes * 8))
        num = ''.join(self.binStringList[varStartPos:varStartPos+varLen])
        print("Parser variable", int(num, 2) + varOffset)

    def parsePayload(self, enablePrint):                          #if print 1 then print parsed payload
        self.binStringList = list(bin(int(self.inputString, self.base))[2:].zfill(self.numOfBytes * 8))

        self.index = int(''.join(self.binStringList[self.indexStart : self.indexStart + self.indexLen]),2)

        # BATERKAAAA ESTE

        self.temp = (int(''.join(self.binStringList[self.tempStart: self.tempStart + self.tempLen]), 2) * self.tempRes) + self.tempOffset
        self.hum = int(''.join(self.binStringList[self.humStart : self.humStart + self.humLen]),2)
        self.dbg = int(''.join(self.binStringList[self.dbgStart: self.dbgStart + self.dbgLen]), 2)

        for i in range(self.pressNum):
            self.press[i] = int(int(''.join(self.binStringList[self.pressBaseStart + (self.pressLen * i) : self.pressBaseStart + (self.pressLen * i) + self.pressLen]),2) + self.pressOffset)

        if enablePrint == 1:
            print("Index: " + str(self.index))
            print("Batt: NONE")
            print("Temp: " + str(self.temp) + "C")
            print("Hum: " + str(self.hum) + "%")

            for i in range(self.pressNum):
                print("Press_"+ str(i) +" "+ str(self.press[i]) + "Pa")

            print("DBG:", self.dbg)



d = decoder("06CB52448C62443123D8922C48EA161A",16)
d.parsePayload(1)
