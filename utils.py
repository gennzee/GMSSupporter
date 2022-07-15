import cv2

#################################
#           CONSTANTS           #
#################################
MONITOR = {'top': 0, 'left': 0, 'width': 1366, 'height': 768}
DEFAULT_MOVE_TOLERANCE = 0.08
DEFAULT_ADJUST_TOLERANCE = 0.01

#################################
#         Bot Settings          #
#################################
move_tolerance = DEFAULT_MOVE_TOLERANCE
adjust_tolerance = DEFAULT_ADJUST_TOLERANCE

#################################
#       Global Variables        #
#################################
calibrated = False
ready = False
enabled = False
player_pos = (0,0)
target = (0,0)
sequence = []
seq_index = 0
file_index = 0
new_point = None
eboss_active = False
rune_index = 0
rune_active = False
rune_pos = (0, 0)

#################################
#       Class Variables         #
#################################
commands = None
capturee = None
bott = None

#################################
#       Capture                 #
#################################
MINIMAP_TOP_BORDER = 20
MINIMAP_BOTTOM_BORDER = 8

minimap_template = cv2.imread('assets/minimap_template.jpg', 0)
player_template = cv2.imread('assets/player_template.png', 0)
rune_template = cv2.imread('assets/rune_template2.png', 0)
rune_buff_template = cv2.imread('assets/rune_buff_template.jpg', 0)
eboss_template = cv2.imread('assets/eboss_template2.jpg', 0)