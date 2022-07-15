from keyboards.arduinoKeys import press, key_down, key_up, releaseAll
#from keyboards.vkeys import press, key_down, key_up
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
            press('x', 1, down_time=0.03, up_time=0.03)
            press('d', 1, down_time=0.03, up_time=0.03)
            press('v', 1, down_time=0.03, up_time=0.03)
            key_up(direction)
            time.sleep(0.62)
        return act

    def jumpUp(self, direction=None):
        def act():
            press("x", 1, down_time=0.03, up_time=0.03)
            time.sleep(0.2)
            key_down(direction)
            press("x", 1, down_time=0.03, up_time=0.03)
            key_up(direction)
            time.sleep(0.9)
        return act

    def jumpDown(self, direction=None):
        def act():
            key_down(direction)            
            press('x', 1, down_time=0.03, up_time=0.03)
            key_up(direction)
            time.sleep(0.7)
        return act

    def keyPress(self, key):
        def act():
            press(key, 1, 0.05, 0.05)
        return act

    def keyDown(self, key):
        def act():
            key_down(key)
        return act

    def keyUp(self, key):
        def act():
            key_up(key)
        return act

    def sleep(self, sleep_time):
        def act():
            time.sleep(sleep_time)
        return act

    def adjust(self, target, tolerance=utils.adjust_tolerance):
        def act():
            while abs(utils.player_pos[0] - target[0]) > 0.005:
                if utils.player_pos[0] > target[0]:
                    press('left', 1, down_time=0.005, up_time=0.001)
                else:
                    press('right', 1, down_time=0.005, up_time=0.001)
        return act