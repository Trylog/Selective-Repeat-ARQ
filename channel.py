import komm
import numpy as np
from typing import List

class Channel:

    probability = 10

    def __init__(self):
        self._buffer = None
        self._currentIndex = 0
        self._nextOut = 0
        self._currentModel = 0

    def bsc(self, probability, packet):
        bsc = komm.BinarySymmetricChannel(probability)
        return bsc(packet)

    def gilbert_elliott(self, transmited_signal, p_bg, p_gb, num_bits):
        channel_state = [1]  # start in the good state
        for i in range(num_bits - 1):
            if channel_state[-1] == 1:
                if np.random.rand() < p_gb:
                    channel_state.append(0)
                else:
                    channel_state.append(1)
            else:
                if np.random.rand() < p_bg:
                    channel_state.append(1)
                else:
                    channel_state.append(0)
        error_sequence = []
        for state in channel_state:
            if state == 1:
                error_sequence.append(np.random.binomial(1, 1e-4))
            else:
                error_sequence.append(np.random.binomial(1, 1e-2))

        #transmitted_signal = np.random.binomial(1, 0.5, num_bits)
        received_signal = np.bitwise_xor(transmited_signal, error_sequence)

        return transmited_signal, received_signal

    def gem(self, probability, packet):
        return

    def chIn(self,  chInput: List[int]) -> None:
        self._buffer = []
        if self._currentModel:
            self._buffer.append(self.gilbert_elliott(chInput, 1e-3, 1e-3, len(chInput)))
        else:
            self._buffer.append(self.bsc(self.probability, chInput))

    def chOut(self):
        if self._nextOut <= len(self._buffer):
            self._nextOut += 1
            return self.buffer[self._nextOut]

    def setModel(self, model):
        self._currentModel=model
