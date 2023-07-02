import time

import numpy as np

import channel
import random
import threading
import main

lock = threading.Lock()


class Transmitter:

    def __init__(self, transmission, arq, coding, numberOfPackets):
        self.data = None
        self.codingType = None
        self.packetLenght = None
        self.transmission = transmission
        self.arq = arq
        self.coding = coding
        self.numberOfPackets = numberOfPackets
        self.currentPacketNumber = 0

    def start(self):
        print('transmiter start')
        if self.arq == 1:
            while self.numberOfPackets > 0:
                print('numer pakietu t: '+str(self.numberOfPackets))
                transmissionCP = ""
                ciag = ""
                isReapeted = False
                for _ in range(256):
                    losowa_liczba = random.randint(0, 1)
                    ciag += str(losowa_liczba)
                codeData = self.codeHamming(ciag)
                packet = ""
                #packet += isReapeted
                packet += codeData
                lock.acquire()
                self.transmission = channel.bsc(0.1, packet)
                lock.release()
                time.sleep(1)
                lock.acquire()
                transmissionCP = self.transmission
                lock.release()
                if main.repeater != 0:   # check czy hamming wykryl, tu ma być  self.errorHamming(transmissionCP)
                    isReapeted = True
                    codeData = self.codeHamming(ciag)
                    packet = ""
                    #packet += isReapeted
                    packet += codeData
                    lock.acquire()
                    self.transmission = channel.bsc(0.1, packet)
                    lock.release()
                    time.sleep(1)
                self.numberOfPackets -= 1
        else:
            if self.numberOfPackets % 1000 == 0:
                numberOfBlocks = self.numberOfPackets / 1000
            else:
                numberOfBlocks = self.numberOfPackets / 1000 + 1

            for j in range(int(numberOfBlocks)):
                for i in range(1000):
                    ciag = ""
                    for _ in range(256):
                        losowa_liczba = random.randint(0, 1)
                        ciag += str(losowa_liczba)
                    codeData = self.codeHamming(ciag)
                    packet = ""
                    packet += str(i)
                    if j * 1000 + i == self.numberOfPackets - 1:
                        packet += str(0)
                    else:
                        packet += str(1)
                    packet += codeData
                    lock.acquire()

                    self.transmission = channel.bsc(0.1, packet)
                    lock.release()
                    time.sleep(1)

        def crc_checksum(data, polynomial):
            crc_value = self.crc1(data, polynomial)
            return crc_value.to_bytes(1, byteorder='big')

        def crc1(data, polynomial):
            crc = 0
            for byte in data:
                crc ^= byte
                for _ in range(8):
                    if crc & 0x80:
                        crc = (crc << 1) ^ polynomial
                    else:
                        crc <<= 1
                    crc &= 0xFF  # Ograniczenie wartości CRC do 8 bitów (jednego bajtu)
            return crc




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
                if k > len(data):
                    return res[::-1]

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
