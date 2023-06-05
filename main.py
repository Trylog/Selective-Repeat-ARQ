# This is a sample Python script.
import sys
import numpy as np
# from numpy   import long
import threading
import time

import receiver
import transmitter

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
menu_options1 = {
    1: 'ARQ step and wait',
    2: 'ARQ selective repeat',
    3: 'Wyjście',
}

menu_options2 = {
    1: 'BST',
    2: 'Geblerta-Eliota',
}


def menu():
    while (True):
        print('Wybierz typ ARQ')
        print_menu(1)
        option1 = int(input('Wybrano: '))
        print('Wybierz typ kanału')
        print_menu(2)
        option2 = int(input('Wybrano: '))
        if option1 == 3:
            return 0, 0;
        elif option1 == 1 or option1 == 2:
            if option2 == 1 or option2 == 2:
                return option1, option2
        else:
            print('Podano złe wartości')


def print_menu(i):
    if i == 1:
        for key in menu_options1.keys():
            print(key, ':', menu_options1[key])
    if i == 2:
        for key in menu_options2.keys():
            print(key, ':', menu_options2[key])


def constRec(transmission, arq, coding, numberOfPackets):
    rec = receiver.Receiver(transmission, arq, coding, numberOfPackets)
    recS = rec.start()

def constTrans(transmission, arq, coding, numberOfPackets):
    trans = transmitter.Transmitter(transmission, arq, coding, numberOfPackets)
    transS = trans.start()


if __name__ == '__main__':
    # data = bytes([1, 2, 3, 4])
    # print(sys.getsizeof(data))

    options = menu()
    coding = options[2]
    chanel = options[1]
    arq = options[0]
    numberOfPackets = options[3]

    transmission = ""
    thread0 = threading.Thread(target=constRec(transmission, arq, coding, numberOfPackets))
    thread0.start()
    thread1 = threading.Thread(target=constTrans(transmission, arq, coding, numberOfPackets))
    thread1.start()

# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
