class Receiver:
    def __init__(self):
        self.packetsRec = []
        self.packetsWithErrors = []
        self.packetLenght = None

    def parityBitDecoding(self, current):
        parityBit = self.packets[current][self.packetLenght - 1]
    def requestPacketRetransmit(self, number):
