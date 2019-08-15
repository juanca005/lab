#!/usr/bin/python3
""" TP2 para ejercitar sincronizacion y sus problemas"""
import threading
import time
import random
from threading import Barrier
from threading import Semaphore
from threading import Event

lugares_bote = []
viajes = 0

barrier= Barrier(4)
mutex=Semaphore(1)
hincha_river=0
hinca_boca=0
hincha_riverQueue=Semaphore(0)
hincha_bocaQueue=Semaphore(0)
isCaptain = False

def hincha_river():
    """ Implementar funcion para subir al bote ....si es que se puede ..."""
    mutex.wait()
    hincha_river += 1
    if hincha_river == 4:
        hincha_riverQueue.signal(4)
        hincha_river=0
        isCaptain= True
    elif hincha_river == 2 and hincha_boca >=2:
        hincha_riverQueue.signal(2)
        hincha_bocaQueue.signal(2)
        hincha_boca -= 2
        hincha_river = 0
        isCaptain = True
    else:
        mutex(signal)
        hincha_riverQueue.wait()
    a_bordo()
    barrier.wait()

    if isCaptain:
        a_remar()
        mutex.signal()

    print("vamos river")



def hincha_boca():
    """ Implementar funcion para subir al bote ....si es que se puede ..."""
    print("vamos boca")


def barra_brava_river():
    """ Generacion de hinchas de River"""
    while viajes < 20:
        time.sleep(random.randrange(0, 5))
        r = threading.Thread()
        r.start()

def barra_brava_boca():
    """ Generacion de hinchas de Boca"""
    while viajes < 20:
        time.sleep(random.randrange(0, 5))
        b = threading.Thread()
        b.start()


t1 = threading.Thread(name="hinchaRiver", target=hincha_river)
t2 = threading.Thread(name="hinchaBoca", target=hincha_boca)
t1.start()
t2.start()
t1.join()
t2.join()

print("terminaron los viajes ")