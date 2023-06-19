import time
import channel
import random
import threading
import queue
from crc import Calculator, Crc32

lock = threading.Lock()


class Transmitter:

    def __init__(self, transmission, arq, coding, numberOfPackets, transmissionOrg):
        self.data = None
        self.codingType = None
        self.packetLenght = None
        self.numberOfPackets = None
        self.transmission = transmission
        self.arq = arq
        self.coding = coding
        self.numberOfPackets = numberOfPackets
        self.currentPacketNumber = 0
        self.transmissionOrg = transmissionOrg

    def start(self):
        print("transmiter start")
        if self.arq == 1:
            while self.numberOfPackets:
                print("transmiting first packed")
                transmissionCP = ""
                ciag = ""
                isReapeted = 0
                for _ in range(256):
                    losowa_liczba = random.randint(0, 1)
                    ciag += str(losowa_liczba)
                with lock:
                    self.transmissionOrg = ciag
                #codeData = self.codeHamming(ciag)
                packet = ""
                packet += str(isReapeted)
                #packet += codeData
                packet += ciag
                #self.transmission = channel.bsc(0.1, packet)
                with lock:
                    self.transmission = packet
                time.sleep(1)
                with lock:
                    transmissionCP = self.transmission
                while transmissionCP != 1:
                    print("przyszła informacja o błędzie transmisji - retransmisja")
                    isReapeted = 1
                    #codeData = self.codeHamming(ciag)
                    packet = ""
                    packet += str(isReapeted)
                    #packet += codeData
                    packet += ciag

                    #self.transmission = channel.bsc(0.1, packet)
                    with lock:
                        self.transmission = packet

                    time.sleep(1)
                    with lock:
                        transmissionCP = self.transmission
                self.numberOfPackets -= 1
                time.sleep(10)
        else:
            """
            if self.numberOfPackets % 1000 == 0:
                numberOfBlocks = self.numberOfPackets / 1000
            else:
                numberOfBlocks = self.numberOfPackets / 1000 + 1

            for j in range(numberOfBlocks):
                for i in range(1000):
                    ciag = ""
                    for _ in range(256):
                        losowa_liczba = random.randint(0, 1)
                        ciag += str(losowa_liczba)
                    codeData = self.codeHamming(ciag)
                    packet = ""
                    packet += i  # TODO change to binary
                    if j * 1000 + i == self.numberOfPackets - 1:
                        packet += 0  # TODO change to binary
                    else:
                        packet += 1  # TODO change to binary
                    packet += codeData
                    lock.acquire()
                    self.transmission = channel.bsc(0.1, packet)
                    lock.release()
                    time.sleep(1)
                # TODO receiving repeat requests
                """


    def parityBitCoding(self):
        numberOfPackets = self.numberOfPackets

        ##długość paczki trzeba dstosować do konkrętnego kodu
        ##dwa rodzaje arq
        ##crc różne
        # historia kanału  -gilbertta-elia dasch7 hard lorawan

    def codeCRC(self, data):
        calculator = Calculator(Crc32.CCITT)
        dataC = bytes(data)
        checkSum = calculator.checksum(dataC)
        dataC += checkSum
        return dataC

    def calcRedundantBits(self, m):
        for i in range(m):
            if (2 ** i >= m + i + 1):
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
