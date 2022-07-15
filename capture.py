import threading
import mss
import utils
import numpy as np
import cv2
import point
import bot

class Capture:
    def __init__(self):
        self.cap = threading.Thread(target=self.capture)
        self.cap.daemon = True

    def capture(self):
        with mss.mss() as sct:
            print('Started capture')
            while True:
                frame = np.array(sct.grab(utils.MONITOR))
                if not utils.calibrated:
                    # Get the bottom right point of the minimap
                    _, br = Capture.single_match(frame[:round(frame.shape[0] / 4),:round(frame.shape[1] / 4)], utils.minimap_template)
                    mm_tl, mm_br = (utils.MINIMAP_BOTTOM_BORDER, utils.MINIMAP_TOP_BORDER), (tuple(max(75, a - utils.MINIMAP_BOTTOM_BORDER) for a in br))      # These are relative to the entire screenshot
                    utils.calibrated = True
                else:
                    # Crop the frame to only show the minimap
                    minimap = frame[mm_tl[1]:mm_br[1], mm_tl[0]:mm_br[0]]
                    player = Capture.multi_match(minimap, utils.player_template, threshold=0.9)
                    if player:
                        utils.player_pos = Capture.convert_to_relative(player[0], minimap)        
                       
                    # Check for eboss warning
                    height, width, _ = frame.shape
                    eboss_frame = frame[height//4:3*height//4, width//4:3*width//4]
                    if not utils.eboss_active and Capture.multi_match(eboss_frame, utils.eboss_template, threshold=0.9):
                        utils.eboss_active = True

                    # Check for a rune
                    if not utils.rune_active:
                        rune = Capture.multi_match(minimap, utils.rune_template, threshold=0.9)
                        if rune and utils.sequence:
                            utils.rune_pos = Capture.convert_to_relative((rune[0][0] - 1, rune[0][1]), minimap)
                            distances = list(map(lambda p: bot.Bot.distance(utils.rune_pos, p.location) if isinstance(p, point.Point) else float('inf'), utils.sequence))
                            utils.rune_index = np.argmin(distances)
                            utils.rune_active = True

                    # Draw point
                    if not utils.enabled:
                        color = (0, 0, 255)
                    else:
                        color = (0, 255, 0)
                    for element in utils.sequence:
                        if isinstance(element, point.Point):
                            cv2.circle(minimap, (round((mm_br[0] - mm_tl[0]) * element.location[0]), round((mm_br[1] - mm_tl[1]) * element.location[1])), round(minimap.shape[1] * utils.move_tolerance), color, 1)

                    if utils.ready:
                        cv2.circle(minimap, Capture.convert_to_absolute(utils.player_pos, minimap), 3, (255, 0, 0), -1)

                    minimap = Capture.rescale_frame(minimap, 2.0)
                    cv2.imshow('mm', minimap)
                if cv2.waitKey(1) & 0xFF == 27:     # 27 is ASCII for the Esc key
                    break

    def rescale_frame(frame, percent=1.0):
        width = int(frame.shape[1] * percent)
        height = int(frame.shape[0] * percent)
        return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    def convert_to_relative(point, frame):
        return (point[0] / frame.shape[1], point[1] / frame.shape[0])
        
    def convert_to_absolute(point, frame):
        return tuple(int(round(point[i] * frame.shape[1 - i])) for i in range(2))

    def single_match(frame, template):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        top_left = max_loc
        w, h = template.shape[::-1]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        return top_left, bottom_right

    def multi_match(frame, template, threshold=0.63):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        return [tuple(int(round(p[i] + template.shape[1 - i] / 2))
                      for i in range(2))
                for p in locations]
