import utils
import csv
from os import listdir
from os.path import isfile, join
import winsound
import time
import point

def load(index=float('inf')):    
    utils.sequence = []
    path = './bots'
    csv_files = [f for f in listdir(path) if isfile(join(path, f)) and '.csv' in f]
    if not csv_files:
        print('Unable to find a .csv bot file')
    else:
        print('\n\n\n~~~ Loading File ~~~')
        print('Select from the following bot files:')
        for i in range(len(csv_files)):
            print(f'{i}  {csv_files[i]}')
        print('')
        while index not in range(len(csv_files)):
            selection = input('>>> ')
            if selection in ['^C', '^Z']:
                break
            try:
                index = int(selection)
            except:
                print('Selection must be an integer')
        utils.file_index = index

        # Load the file specified by the user.
        with open(join(path, csv_files[index])) as f:
            first_row = True
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    try:
                        for setting in row:
                            settingArr = setting.split('=')
                            name = settingArr[0]
                            value = settingArr[1]
                            if setting != "default":
                                exec(f'utils.{setting}')                      
                        continue
                    except:
                        print(f"Skipped loading first row due to invalid bot settings: '{row}'")

                if len(row) == 1:
                    # If there is only one element in the row, it must be a label
                    utils.sequence.append(row[0])
                else:                    
                    pos = tuple([row[i] for i in range(len(row))])
                    if (pos[0] == 0 and pos[1] == 0):
                        continue

                    args = ''.join([row[i] + (', ' if i != len(row) - 1 else '') for i in range(len(row))])
                    try:
                        exec(f'utils.new_point = point.Point({args})')
                    except:
                        print(f"Error while creating point 'Point({args})'")
                        continue
                    utils.sequence.append(utils.new_point)
                    
        print(f'Finished loading file at index {index}')
        winsound.Beep(523, 200)
        winsound.Beep(659, 200)
        winsound.Beep(784, 200)
        time.sleep(0.15)