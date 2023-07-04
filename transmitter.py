import time
import channel
import random
import threading
import queue


import main

class Transmitter:

    def __init__(self, transmission, arq, coding, numberOfPackets, transmissionOrg):
        self.data = None
        self.codingType = None
        self.packetLenght = None
        self.lastTransmission = None
        self.numberOfPackets = None
        self.transmission = transmission
        self.arq = arq
        self.coding = coding
        self.numberOfPackets = numberOfPackets
        self.currentPacketNumber = 0
        self.transmissionOrg = transmissionOrg
        self.numberOfRetransmits = 0
        self.a = 0

    def start(self):
        print("transmiter start")
        if self.arq == 1:
            transmissionCP = ""
            while self.numberOfPackets > 0:

                ciag = ""
                isReapeted = 0
                for _ in range(2088):
                    losowa_liczba = random.randint(0, 1)
                    ciag += str(losowa_liczba)
                packet = ""
                # packet = "packet"
                # packet += str(self.numberOfPackets)
                # packet += str(isReapeted)
                if self.coding == 2:
                    packet += self.codeHamming(ciag)
                elif self.coding == 3:
                    packet += self.parityBitCoding(ciag)
                elif self.coding == 1:
                    packet += self.encode_message(ciag)

                withErrors = channel.bsc_transmit(packet, 0.0002)
                if withErrors != packet:
                    self.a += 1
                self.transmission.put(withErrors)
                self.lastTransmission = packet
                print("transmiting packet: " + str(self.numberOfPackets))
                time.sleep(0.5)
                transmissionCP = self.transmission.get()
                self.transmission.put(transmissionCP)
                self.transmission.task_done()
                print("potwierdzenie: " + transmissionCP)
                while transmissionCP != '1':
                    self.numberOfRetransmits += 1
                    print("przyszła informacja o błędzie transmisji - retransmisja")
                    isReapeted = 1
                    packet = ""
                    # packet += str(isReapeted)
                    if self.coding == 2:
                        packet += self.codeHamming(ciag)
                    elif self.coding == 3:
                        packet += self.parityBitCoding(ciag)
                    elif self.coding == 1:
                        packet += self.encode_message(ciag)

                    withErrors = channel.bsc_transmit(packet, 0.0002)
                    if withErrors != packet:
                        self.a += 1
                    self.transmission.put(withErrors)
                    time.sleep(0.5)
                    transmissionCP = self.transmission.get()
                    self.transmission.put(transmissionCP)
                    self.transmission.task_done()
                self.numberOfPackets -= 1
            print('liczba retransmisji: ' + str(self.numberOfRetransmits))
            print('liczba faktycznych błędów: ' + str(self.a))
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


    def crc32(self, data):
        crc = 0xFFFFFFFF
        for bit in data:
            crc ^= int(bit)
            for _ in range(8):
                crc = (crc >> 1) ^ 0xEDB88320 if crc & 1 else crc >> 1
        return crc ^ 0xFFFFFFFF

    def encode_message(self, message):
        crc_value = self.crc32(message)
        encoded_message = message + format(crc_value, '032b')
        return encoded_message

    def detect_errors(self, received_message):
        crc_value = received_message[-32:]
        message = received_message[:-32]
        calculated_crc = self.crc32(message)
        return crc_value != format(calculated_crc, '032b')

    def parityBitCoding(self, string):
        out = ""
        out = string
        numberOfPositives = 0
        for bit in string:
            if bit == '1':
                numberOfPositives += 1
        out += str(numberOfPositives % 2)
        return out

    def parityBitCheck(self, string):
        out = ""
        out = string[0:-1]
        numberOfPositives = 0
        for bit in out:
            if bit == '1':
                numberOfPositives += 1
        if str(numberOfPositives % 2) == string[-1]:
            return True
        else:
            return False



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
