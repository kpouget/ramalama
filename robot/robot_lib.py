import time
import logging
import sys
import atexit
from multiprocessing import freeze_support
freeze_support()

try:
    from mBot import mBot
except ImportError:
    logging.warning("mbot library not available. Mimicking the operations.")
    mBot = None

def _at_exit():
    logging.warning("Disconnecting ...")
    bot.exit(0,0)

if mBot:
    bot = mBot()
    bot.startWithBle()
    atexit.register(_at_exit)

def move(lenght, left, right):
    bot.doMove(left, right)
    time.sleep(lenght)
    bot.doMove(0,0)

def beep():
    tones ={"C3":131,"D3":147,"E3":165,"F3":175,"G3":196,"A3":220,"B3":247,
	    "C4":262,"D4":294,"E4":330,"F4":349,"G4":392,"A4":440,"B4":494,
	    "C5":523,"D5":587,"E5":659,"F5":698,"G5":784,"A5":880,"B5":988}

    for _ in range(3):
        bot.doBuzzer(tones["F4"], 1)
        time.sleep(1.1)

    bot.doBuzzer(tones["F4"], 4)
    time.sleep(2)
