import threading
import mss
import keyboard as kb
import time
import utils
import point
from keyboards.arduinoKeys import press
#from keyboards.vkeys import press
from csvLoader import load
import winsound
import math
from playsound import playsound

class Bot:
    def __init__(self):
        self.cap = threading.Thread(target=self.bot)
        self.cap.daemon = True

    def bot(self):
        print('Started bot')

        cadena_voidStrike = Bot.buff(162, buffs=['home'])
        cadena_veteranShadowDealer = Bot.buff(185, buffs=['del'])
        cadena_shadowDealerElixir = Bot.buff(125, buffs=['2'])
        cadena_booster = Bot.buff(170, buffs=['8'])
        cadena_mapleWarrior = Bot.buff(800, buffs=['9'])        
        cadena_holySymbol = Bot.buff(185, buffs=['3'])
        cadena_sharpEye = Bot.buff(185, buffs=['4'])

        darkServant = Bot.buff(170, buffs=['lshift'])
        throwingBooster = Bot.buff(170, buffs=['insert'])
        mapleWarrior = Bot.buff(800, buffs=['home'])
        holySymbol = Bot.buff(185, buffs=['del'])
        decentSharpEye = Bot.buff(185, buffs=['end'])

        with mss.mss() as sct:
            while True:
                Bot.checkForElite()
                Bot.checkForRune()
                Bot.checkUserInput()                
                if utils.enabled and len(utils.sequence) > 0:
                    curr_index = utils.seq_index
                    curr_time = time.time()

                    cadena_voidStrike = cadena_voidStrike(curr_time)
                    cadena_veteranShadowDealer = cadena_veteranShadowDealer(curr_time)
                    cadena_booster = cadena_booster(curr_time)
                    cadena_mapleWarrior = cadena_mapleWarrior(curr_time)
                    # cadena_shadowDealerElixir = cadena_shadowDealerElixir(curr_time)
                    # cadena_holySymbol = cadena_holySymbol(curr_time)
                    # cadena_sharpEye = cadena_sharpEye(curr_time)
                    # darkServant = darkServant(curr_time)
                    # throwingBooster = throwingBooster(curr_time)
                    # mapleWarrior = mapleWarrior(curr_time)
                    # holySymbol = holySymbol(curr_time)
                    # decentSharpEye = decentSharpEye(curr_time)

                    element = utils.sequence[curr_index]
                    if isinstance(element, point.Point):
                        print(element)
                        element.execute()
                        if utils.enabled:
                            utils.seq_index = (utils.seq_index + 1) % len(utils.sequence)
                    else:
                        utils.seq_index = (utils.seq_index + 1) % len(utils.sequence)
                else:
                    time.sleep(0.1)

    def buff(period, buffs=['0'], t=0, mode=0):        
        if len(buffs) == 0:
            return print("Function 'main_buff' requires at least one buff")
        def act(new_t):
            nonlocal buffs          
            if mode == 0:
                if t == 0 or new_t - t > period:
                    for b in buffs:
                        print("Buff")
                        time.sleep(0.6)
                        press(b, 1, down_time=0.5, up_time=0.3)
                else:
                    new_t = t
            elif mode == 1:
                if t == 0 or new_t - t > period / len(buffs):
                    press(buffs[0], 3, down_time=0.5, up_time=0.05)
                    time.sleep(0.05)
                    buffs = buffs[1:] + buffs[:1]
                else:
                    new_t = t
            return Bot.buff(period, buffs=buffs, t=new_t, mode=mode)
        return act

    def checkUserInput():
        # Check for user input
        if kb.is_pressed('F5'):
            Bot.toggle_enabled()
        elif kb.is_pressed('F6'):
            Bot.recalibrate_mm()
            load(index=utils.file_index)
        elif kb.is_pressed('F7'):
            Bot.recalibrate_mm()
            load()
        elif kb.is_pressed('F8'):
            displayed_pos = tuple('{:.3f}'.format(round(i, 3)) for i in utils.player_pos)
            print('\n\n\nCurrent position: ({}, {})'.format(displayed_pos[0], displayed_pos[1]))
            time.sleep(1)  

    def toggle_enabled():
        Bot.reset_rune()
        Bot.reset_eboss()
        prev = utils.enabled
        if not utils.enabled:
            winsound.Beep(784, 333)     # G5
        else:
            winsound.Beep(523, 333)     # C5
        utils.enabled = not utils.enabled
        print(f"\n\n\ntoggled: {'on' if prev else 'off'} --> {'ON' if utils.enabled else 'OFF'}")
        time.sleep(0.667)

    def recalibrate_mm():
        utils.calibrated = False

    def checkForElite():
        # Check for elite
        if utils.eboss_active:
            utils.enabled = False
            while not kb.is_pressed('F5'):
                playsound('assets/beedo.mp3')
                time.sleep(0.1)
            utils.eboss_active = False
            time.sleep(1)

    def checkForRune():
        # Check for rune
        if utils.rune_active:
            utils.enabled = False
            while not kb.is_pressed('F5'):
                playsound('assets/beedo.mp3')
                time.sleep(0.1)
            utils.rune_active = False
            time.sleep(1)

    def reset_eboss():
        utils.eboss_active = False

    def reset_rune():
        utils.rune_active = False

    def distance(a, b):
        return math.sqrt(sum([(a[i] - b[i]) ** 2 for i in range(2)]))

    def move(target, tolerance=utils.move_tolerance, max_steps=15):
        prev_pos = [tuple(round(a, 2) for a in utils.player_pos)]
        while utils.enabled and max_steps > 0 and Bot.distance(utils.player_pos, target) > tolerance:
            if kb.is_pressed('F5'):
                Bot.toggle_enabled()
                break

            #while abs(utils.player_pos[0] - target[0]) > tolerance / math.sqrt(2):
            while abs(utils.player_pos[0] - target[0]) > utils.move_tolerance:
                if kb.is_pressed('F5'):
                    Bot.toggle_enabled()
                    break
                if utils.player_pos[0] < target[0]:     
                    print("Jump right")
                    utils.commands.jump("right", target)()
                else:
                    print("Jump left")
                    utils.commands.jump("left", target)()
                max_steps -= 1
            
            #while abs(utils.player_pos[1] - target[1]) > tolerance / math.sqrt(2):
            while abs(utils.player_pos[1] - target[1]) > utils.move_tolerance:
                if kb.is_pressed('F5'):
                    Bot.toggle_enabled()
                    break
                
                if utils.player_pos[1] < target[1]:
                    print("jump down")
                    utils.commands.jumpDown('down')()
                else:
                    #commands.jump('up')()
                    print("jump up")
                    utils.commands.jumpUp('up')()
                max_steps -= 1
            
            rounded_pos = tuple(round(a, 2) for a in utils.player_pos)
            num_previous = prev_pos.count(rounded_pos)
            if num_previous > 0 and num_previous % 2 == 0:
                print('stuck')
                for _ in range(10):
                    press('left', 1, up_time=0.05)
                    press('right', 1, up_time=0.05)
            prev_pos.append(rounded_pos)
            if len(prev_pos) > 3:
                prev_pos.pop(0)
        return max_steps