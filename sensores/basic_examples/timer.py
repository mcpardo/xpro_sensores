# publisher
import time
import sys
import threading

def issr():
    print("Hola")
    timerObject = threading.Timer(10, issr)
    timerObject.start()

issr()
