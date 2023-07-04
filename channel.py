import random
import numpy as np
from typing import List



def bsc_transmit(input_string, error_probability):
    output_string = ""
    for bit in input_string:
        # Losowe przekształcenie bitu
        if random.random() < error_probability:
            # Zmiana bitu
            output_bit = '1' if bit == '0' else '0'
        else:
            # Brak zmiany bitu
            output_bit = bit
        output_string += output_bit
    return output_string
class Channel:

    probability = 10

    def __init__(self):
        self._buffer = None
        self._currentIndex = 0
        self._nextOut = 0
        self._currentModel = 0


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


