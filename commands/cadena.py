from keyboards.arduinoKeys import press, key_down, key_up, releaseAll
import time
import utils

class Commands:
    def goto(self, label):
        def act():
            try:
                utils.seq_index = utils.sequence.index(label)
            except:
                print(f"Label '{label}' does not exist")
        return act

    def wait(self, duration):
        def act():
            time.sleep(duration)
        return act
    
    def walk(self, direction, duration):
        def act():
            press(direction, 1, down_time=duration, up_time=0.05)
        return act

    def jump(self, direction, target):
        def act():
            key_down(direction)
            press('alt', 1, down_time=0.03, up_time=0.03)
            press('x', 1, down_time=0.03, up_time=0.03)
            press('a', 1, down_time=0.03, up_time=0.03)
            key_up(direction)
            isTrigger = False
            for i in range(10): #similar to time.sleep(0.7)
                if abs(utils.player_pos[0] - target[0]) < 0.03 and not isTrigger:
                    isTrigger = True
                    press('q', 2, down_time=0.024, up_time=0.015)
                time.sleep(0.063)
        return act

    def jumpUp(self, direction="up"):
        def act():
            press("alt", 1, down_time=0.03, up_time=0.03)
            key_down(direction)
            press('alt', 1, down_time=0.03, up_time=0.03)
            key_up(direction)
            time.sleep(0.9)
        return act

    def jumpDown(self, direction="down"):
        def act():
            key_down(direction)
            press('alt', 1, down_time=0.03, up_time=0.03)
            #press('e', 1, down_time=0.03, up_time=0.03)
            key_up(direction)
            time.sleep(0.7)
        return act

    def keyPress(self, key, down_time=0.05, up_time=0.05):
        def act():
            press(key, 1, down_time, up_time)
        return act

    def keyDown(self, key):
        def act():
            key_down(key)
        return act

    def keyUp(self, key):
        def act():
            key_up(key)
        return act

    def releaseAll(self):
        def act():
            releaseAll()
        return act

    def sleep(self, sleep_time):
        def act():
            time.sleep(sleep_time)
        return act

    def adjust(self, target, tolerance=utils.adjust_tolerance):
        def act():
            while abs(utils.player_pos[0] - target[0]) > 0.007:
                if utils.player_pos[0] > target[0]:
                    press('left', 1, down_time=0.0100, up_time=0.001)
                else:
                    press('right', 1, down_time=0.0100, up_time=0.001)                    
                time.sleep(1/1000)

            while abs(utils.player_pos[0] - target[0]) > 0.001:
                if utils.player_pos[0] > target[0]:
                    press('left', 1, down_time=0.0100, up_time=0.001)
                else:
                    press('right', 1, down_time=0.0100, up_time=0.001)                    
                time.sleep(30/1000)
        return act