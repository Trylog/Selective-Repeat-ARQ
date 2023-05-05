class Transmitter:

    def __init__(self):
        self.data = None
        self.codingType = None
        self.packetLenght = None
        self.numberOfPackets = None

    def parityBitCoding(self):
        numberOfPackets = self.numberOfPackets


        ##długość paczki trzeba dstosować do konkrętnego kodu
        ##dwa rodzaje arq
        ##crc różne
        #historia kanału  -gilbertta-elia dasch7 hard lorawan

    def codeCRC(self, data):
        return data

    def codeHamming(self, data):
        return data
