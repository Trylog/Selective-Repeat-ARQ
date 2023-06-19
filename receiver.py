import channel
import threading

lock = threading.Lock()


class Receiver:
    def __init__(self, transmission, arq, coding, numberOfPackets):
        self.packetsRec = []
        self.packetsWithErrors = []
        self.packetLenght = None
        self.transmission = transmission
        self.lastTransmission = ""
        self.arq = arq
        self.coding = coding
        self.decodedData = []
        self.numberOfPackets = numberOfPackets

    def start(self):
        while self.numberOfPackets:
            lock.acquire()
            transmissionCP = self.transmission
            lock.release()
            if transmissionCP == self.lastTransmission:

                if self.errorHamming(transmissionCP) == 0:
                    self.decodedData.append(transmissionCP[0:2088])
                    lock.acquire()
                    self.transmission = 1
                    lock.release()
                    self.numberOfPackets -= 1
                else:
                    lock.acquire()
                    self.transmission = 0
                    lock.release()

    def parityBitDecoding(self, current):
        parityBit = self.packets[current][self.packetLenght - 1]

    def requestPacketRetransmit(self, number):
        return

    def calcRedundantBits(self, m):
        for i in range(m):
            if 2 ** i >= m + i + 1:
                return i

    def Hamminglenght(self):
        m = 2088
        for i in range(m):
            if (2 ** i >= m + i + 1):
                return i + 2088

    def posRedundantBits(self, data, r):
        j = 0
        k = 1
        m = len(data)
        res = ''
        for i in range(1, m + r + 1):
            if (i == 2 ** j):
                res = res + '0'
                j += 1
            else:
                res = res + data[-1 * k]
                k += 1
        return res[::-1]

    def calcParityBits(self, arr, r):
        n = len(arr)
        for i in range(r):
            val = 0
            for j in range(1, n + 1):
                if (j & (2 ** i) == (2 ** i)):
                    val = val ^ int(arr[-1 * j])
                arr = arr[:n - (2 ** i)] + str(val) + arr[n - (2 ** i) + 1:]
        return arr

    def detectError(self, arr, nr):
        n = len(arr)
        res = 0
        for i in range(nr):
            val = 0
            for j in range(1, n + 1):
                if (j & (2 ** i) == (2 ** i)):
                    val = val ^ int(arr[-1 * j])
            res = res + val * (10 ** i)
        return int(str(res), 2)

    def codeHamming(self, data):
        m = 2088
        r = self.calcRedundantBits(m)
        arr = self.posRedundantBits(data, r)
        arr = self.calcParityBits(arr, r)
        return arr

    def errorHamming(self, data):
        m = 2088
        r = self.calcRedundantBits(m)
        correction = 0
        correction = self.detectError(data, r)
        return correction
