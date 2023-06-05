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
