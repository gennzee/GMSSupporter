import utils
import capture
import mss
import time
import utils
from commands.cadena import Commands
#from commands.nightWalker import Commands
import bot
import csvLoader
from windowManager import move_window_top_left

if __name__ == '__main__':
    move_window_top_left()
    
    utils.capturee = capture.Capture()
    utils.capturee.cap.start()
    time.sleep(0.5) # wait for capture to fully start

    utils.commands = Commands()

    utils.bott = bot.Bot()
    utils.bott.cap.start()

    utils.ready = True

    csvLoader.load()

    sct = mss.mss()
    while True:
        time.sleep(1)



