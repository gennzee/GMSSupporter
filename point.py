import utils
import bot

class Point:
    def __init__(self, x, y, counter=0, frequency=1, attacks=1, extras=[]):
        self.location = (x, y)
        self.counter = counter
        self.frequency = frequency
        self.attacks = attacks
        self.extras = extras

    def __str__(self):
        result = 'Point:'
        result += f'\n  location: {self.location}'
        result += f'\n  counter: {self.counter}'
        result += f'\n  extras: {self.extras}'
        return result

    def execute(self):
        executed = False
        if self.counter == 0:
            if not self.location == (0,0):
                bot.Bot.move(self.location)
            if utils.enabled:
                for e in self.extras:
                    exec(f'utils.commands.{e}()')                           
            executed = True
        if utils.enabled:
            self.counter = (self.counter + 1) % self.frequency
        return executed