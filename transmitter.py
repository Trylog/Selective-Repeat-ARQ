

# Developed by Michał Bernacki-Janson


import sys
import numpy as np
# from numpy   import long
import threading
import time
import queue
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
    2: 'Gilberta-Eliota',
}

menu_options3 = {
    1: 'CRC',
    2: 'Hamming',
}


def menu():
    while (True):
        print('Wybierz typ ARQ')
        print_menu(1)
        option1 = int(input('Wybrano: '))
        print('Wybierz typ kanału')
        print_menu(2)
        option2 = int(input('Wybrano: '))
        print('Wybierz typ kodowania')
        print_menu(3)
        option3 = int(input('Wybrano: '))
        print('Ile przesłać pakietów?')
        option4 = int(input('Wybrano: '))
        if option1 == 3:
            return 0, 0, 0, 0;
        elif option1 == 1 or option1 == 2:
            if option2 == 1 or option2 == 2:
                if option3 == 1 or option3 == 2:
                    return option1, option2, option3, option4
                else:
                    print('Podano złe wartości')
            else:
                print('Podano złe wartości')
        else:
            print('Podano złe wartości')


def print_menu(i):
    if i == 1:
        for key in menu_options1.keys():
            print(key, ':', menu_options1[key])
    if i == 2:
        for key in menu_options2.keys():
            print(key, ':', menu_options2[key])
    if i == 3:
        for key in menu_options3.keys():
            print(key, ':', menu_options3[key])


def constRec(que, arq1, coding1, numberOfPackets1, transmissionOrg1):
    rec = receiver.Receiver(que, arq1, coding1, numberOfPackets1, transmissionOrg1)
    recS = rec.start()


def constTrans(que, arq1, coding1, numberOfPackets1, transmissionOrg1):
    trans = transmitter.Transmitter(que, arq1, coding1, numberOfPackets1, transmissionOrg1)
    transS = trans.start()


if __name__ == '__main__':
    # data = bytes([1, 2, 3, 4])
    # print(sys.getsizeof(data))

    # options = menu()
    # coding = options[2]
    # chanel = options[1]
    # arq = options[0]
    # numberOfPackets = options[3]

    print('Setuję wartości')

    # coding 1 - crc; 2 - hamming; 3 - parity bit
    coding = 1
    chanel = 1
    arq = 1
    numberOfPackets = 10

    print('Zaczynam tworzenie wątków')
    print(threading.active_count())

    transmission = queue.LifoQueue()
    transmissionOrg = ""
    thread0 = threading.Thread(target=constRec, args=(transmission, arq, coding, numberOfPackets, transmissionOrg,))
    thread1 = threading.Thread(target=constTrans, args=(transmission, arq, coding, numberOfPackets, transmissionOrg,))

    thread0.start()
    print(threading.active_count())
    thread1.start()
    print(threading.active_count())


