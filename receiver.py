import time

import channel

import queue



class Receiver:
    def __init__(self, transmission, arq, coding, numberOfPackets, transmissionOrg):
        self.packetsRec = []
        self.packetsWithErrors = []
        self.packetLenght = None
        self.transmission = transmission
        self.lastTransmission = ""
        self.arq = arq
        self.coding = coding
        self.decodedData = []
        self.numberOfPackets = numberOfPackets
        self.transmissionOrg = transmissionOrg


    def start(self):
        print("receiver start")
        while self.numberOfPackets > 0:
            # print('rec ch n d')
            transmissionCP = self.transmission.get()
            self.transmission.put(transmissionCP)
            self.transmission.task_done()
            # print('rec got sm')
            while transmissionCP == self.lastTransmission:
                print('pe: ' + transmissionCP)
                if not self.transmission.empty():
                    transmissionCP = self.transmission.get()
                    self.transmission.put(transmissionCP)
                    self.transmission.task_done()
                    print('not empty')

                time.sleep(0.1)
                print('waiting ...')
            print('new transmision detected' + transmissionCP)
            temp = str(transmissionCP)
            """
            tekst = list(temp)
            tekst[3] = '1'
            temp = ''.join(tekst)
            """
            if self.coding == 2:
                print('any error? ' + str(self.errorHamming(temp)))
                if str(self.errorHamming(temp)) == '0':
                    print('uff nie ma błędów')
                    self.transmission.put("1")
                    self.lastTransmission = "1"
                    self.numberOfPackets -= 1
                else:
                    print('proszę o retransmisję')
                    self.transmission.put("0")
                    self.lastTransmission = "0"
            elif self.coding == 3:
                print('any error? ' + str(self.parityBitCheck(temp)))
                if self.parityBitCheck(temp):
                    print('uff nie ma błędów')
                    self.transmission.put("1")
                    self.lastTransmission = "1"
                    self.numberOfPackets -= 1
                else:
                    print('proszę o retransmisję')
                    self.transmission.put("0")
                    self.lastTransmission = "0"
            elif self.coding == 1:
                print('any error? ' + str(self.detect_errors(temp)))
                if not self.detect_errors(temp):
                    print('uff nie ma błędów')
                    self.transmission.put("1")
                    self.lastTransmission = "1"
                    self.numberOfPackets -= 1
                else:
                    print('proszę o retransmisję')
                    self.transmission.put("0")
                    self.lastTransmission = "0"
            print('rec sleep')
            time.sleep(0.2)

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
            if 2 ** i >= m + i + 1:
                return i

    def Hamminglenght(self):
        m = 2088
        for i in range(m):
            if 2 ** i >= m + i + 1:
                return i + 2088

    def posRedundantBits(self, data, r):
        j = 0
        k = 1
        # m = len(data)
        m = 2088
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
