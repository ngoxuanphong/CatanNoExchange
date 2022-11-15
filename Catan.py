import pygame
import numpy as np

PLAYER_COLOR = ['mysticblue', 'gold', 'silver', 'bronze']

RES_NAME = ['lumber', 'brick', 'wool', 'grain', 'ore']

DEV_NAME = ['knight', 'roadbuilding', 'yearofplenty', 'monopoly', 'vp']

pygame.init()
pygame.display.set_mode((1600, 900))

class Image:
    Robber = pygame.transform.smoothscale(
        pygame.image.load('Image/icon_robber.png'), (55, 55))
    Res_card = [pygame.transform.smoothscale(pygame.image.load(
        'Image/card_'+res+'.png'), (43, 60)) for res in RES_NAME+['rescardback', 'rescardoverlimit']]
    Dev_card = [pygame.transform.smoothscale(pygame.image.load(
        'Image/card_'+dev+'.png'), (43, 60)) for dev in DEV_NAME+['devcardback']]

    __img = pygame.image.load('Image/icon_highlight_circle.png')
    Small_highlight_circle = pygame.transform.smoothscale(__img, (40, 40))
    Big_highlight_circle = pygame.transform.smoothscale(__img, (60, 60))

    __img = pygame.image.load('Image/icon_highlight_circle_white.png')
    Small_highlight_circle_white = pygame.transform.smoothscale(
        __img, (40, 40))
    Big_highlight_circle_white = pygame.transform.smoothscale(__img, (60, 60))

    __img = pygame.image.load('Image/bg_button.png')
    Small_button_check = pygame.transform.smoothscale(__img, (40, 40))
    Big_button_check = pygame.transform.smoothscale(__img, (60, 60))
    Big_button_background = Big_button_check.copy()
    Button_roll_dice = Big_button_background.copy()
    __img = pygame.transform.smoothscale(
        pygame.image.load('Image/icon_roll_dice.png'), (50, 50))
    Button_roll_dice.blit(__img, (5, 5))

    __img = pygame.image.load('Image/icon_check.png')
    __img_1 = pygame.transform.smoothscale(__img, (30, 30))
    Small_button_check.blit(__img_1, (5, 5))
    __img_1 = pygame.transform.smoothscale(__img, (45, 45))
    Big_button_check.blit(__img_1, (7.5, 7.5))

    Settlements = []
    Cities = []
    Roads = []

    Dice = [pygame.transform.smoothscale(pygame.image.load(
        'Image/dice_'+str(i)+'.png'), (60, 60)) for i in range(1, 7)]
    Dice.insert(0, 0)

    Largest_army = pygame.transform.smoothscale(
        pygame.image.load('Image/icon_largest_army.png'), (40, 40))
    Largest_army_highlight = pygame.transform.smoothscale(
        pygame.image.load('Image/icon_largest_army_highlight.png'), (40, 40))

    Longest_road = pygame.transform.smoothscale(
        pygame.image.load('Image/icon_longest_road.png'), (40, 40))
    Longest_road_highlight = pygame.transform.smoothscale(
        pygame.image.load('Image/icon_longest_road_highlight.png'), (40, 40))

    Bank = pygame.transform.smoothscale(
        pygame.image.load('Image/bank.png'), (100, 100))

    def set_color(player_color):
        Image.Settlements = [pygame.transform.smoothscale(pygame.image.load(
            'Image/settlement_'+color+'.png'), (55, 55)) for color in player_color]
        Image.Cities = [pygame.transform.smoothscale(pygame.image.load(
            'Image/city_'+color+'.png'), (55, 55)) for color in player_color]
        Image.Roads = [pygame.transform.smoothscale(pygame.image.load(
            'Image/road_'+color+'.png'), (80, 80)) for color in player_color]


Image.set_color(PLAYER_COLOR)

class RGB_color:
    BLACK = (0, 0, 0)
    GRAY = (127, 127, 127)
    WHITE = (255, 255, 255)
    GREEN = (63, 255, 63)
    MAGENTA = (191, 0, 191)
    YELLOW = (191, 191, 0)
    BLUE = (63, 63, 255)
    RED = (255, 63, 63)
    CYAN = (0, 191, 191)
    VIOLET = (127, 0, 255)
    SPRING_GREEN = (127, 255, 0)
    ORANGE = (255, 127, 0)
    OCEAN = (0, 127, 255)
    RASPBERRY = (255, 0, 127)
    TURQUOISE = (0, 255, 127)

class CONST:
    TILE_CENTER_POS = [(1122, 210), (1263, 210), (1334, 331), (1404, 453), (1334, 574), (1263, 696), (1122, 696), (981, 696), (911, 574), (840, 453), (911, 331), (981, 210), (1052, 331), (981, 453), (1052, 574), (1193, 574), (1263, 453), (1193, 331), (1122, 453)]

    ROAD_CENTER_POS = [(1087, 149), (1158, 149), (1193, 210), (1228, 149), (1298, 149), (1334, 210), (1298, 270), (1369, 270), (1404, 331), (1369, 392), (1440, 392), (1475, 452), (1440, 513), (1369, 513), (1404, 574), (1369, 635), (1298, 635), (1334, 696), (1298, 751), (1228, 751), (1193, 696), (1158, 756), (1087, 756), (1052, 696), (1016, 756), (946, 756), (911, 696), (946, 635), (876, 635), (840, 574), (876, 513), (805, 513), (770, 452), (805, 392), (876, 392), (840, 331), (876, 270), (946, 270), (911, 210), (946, 149), (1016, 149), (1052, 210), (1016, 270), (981, 331), (1016, 392), (946, 392), (911, 452), (946, 513), (1016, 513), (981, 574), (1016, 635), (1087, 635), (1122, 574), (1158, 635), (1228, 635), (1263, 574), (1228, 513), (1298, 513), (1334, 452), (1298, 392), (1228, 392), (1263, 331), (1228, 270), (1158, 270), (1122, 331), (1087, 270), (1087, 392), (1052, 452), (1087, 513), (1158, 513), (1193, 452), (1158, 392)]

    POINT_COORDINATE = [(1122, 129), (1193, 169), (1263, 129), (1334, 169), (1334, 250), (1404, 290), (1404, 372), (1475, 412), (1475, 493), (1404, 533), (1404, 615), (1334, 655), (1334, 736), (1263, 766), (1193, 736), (1122, 776), (1052, 736), (981, 776), (911, 736), (911, 655), (840, 615), (840, 533), (770, 493), (770, 412), (840, 372), (840, 290), (911, 250), (911, 169), (981, 129), (1052, 169), (1052, 250), (981, 290), (981, 372), (911, 412), (911, 493), (981, 533), (981, 615), (1052, 655), (1122, 615), (1193, 655), (1263, 615), (1263, 533), (1334, 493), (1334, 412), (1263, 372), (1263, 290), (1193, 250), (1122, 290), (1122, 372), (1052, 412), (1052, 493), (1122, 533), (1193, 493), (1193, 412)]

    TILE_TILE = [(1, 11, 12, 17), (0, 2, 17), (1, 3, 16, 17), (2, 4, 16), (3, 5, 15, 16), (4, 6, 15), (5, 7, 14, 15), (6, 8, 14), (7, 9, 13, 14), (8, 10, 13), (9, 11, 12, 13), (0, 10, 12), (0, 10, 11, 13, 17, 18), (8, 9, 10, 12, 14, 18), (6, 7, 8, 13, 15, 18), (4, 5, 6, 14, 16, 18), (2, 3, 4, 15, 17, 18), (0, 1, 2, 12, 16, 18), (12, 13, 14, 15, 16, 17)]

    POINT_POINT = [(1, 29), (0, 2, 46), (1, 3), (2, 4), (3, 5, 45), (4, 6), (5, 7, 43), (6, 8), (7, 9), (8, 10, 42), (9, 11), (10, 12, 40), (11, 13), (12, 14), (13, 15, 39), (14, 16), (15, 17, 37), (16, 18), (17, 19), (18, 20, 36), (19, 21), (20, 22, 34), (21, 23), (22, 24), (23, 25, 33), (24, 26), (25, 27, 31), (26, 28), (27, 29), (0, 28, 30), (29, 31, 47), (26, 30, 32), (31, 33, 49), (24, 32, 34), (21, 33, 35), (34, 36, 50), (19, 35, 37), (16, 36, 38), (37, 39, 51), (14, 38, 40), (11, 39, 41), (40, 42, 52), (9, 41, 43), (6, 42, 44), (43, 45, 53), (4, 44, 46), (1, 45, 47), (30, 46, 48), (47, 49, 53), (32, 48, 50), (35, 49, 51), (38, 50, 52), (41, 51, 53), (44, 48, 52)]

    TILE_POINT = [(0, 1, 29, 30, 46, 47), (1, 2, 3, 4, 45, 46), (4, 5, 6, 43, 44, 45), (6, 7, 8, 9, 42, 43), (9, 10, 11, 40, 41, 42), (11, 12, 13, 14, 39, 40), (14, 15, 16, 37, 38, 39), (16, 17, 18, 19, 36, 37), (19, 20, 21, 34, 35, 36), (21, 22, 23, 24, 33, 34), (24, 25, 26, 31, 32, 33), (26, 27, 28, 29, 30, 31), (30, 31, 32, 47, 48, 49), (32, 33, 34, 35, 49, 50), (35, 36, 37, 38, 50, 51), (38, 39, 40, 41, 51, 52), (41, 42, 43, 44, 52, 53), (44, 45, 46, 47, 48, 53), (48, 49, 50, 51, 52, 53)]

    POINT_TILE = [(0,), (0, 1), (1,), (1,), (1, 2), (2,), (2, 3), (3,), (3,), (3, 4), (4,), (4, 5), (5,), (5,), (5, 6), (6,), (6, 7), (7,), (7,), (7, 8), (8,), (8, 9), (9,), (9,), (9, 10), (10,), (10, 11), (11,), (11,), (0, 11), (0, 11, 12), (10, 11, 12), (10, 12, 13), (9, 10, 13), (8, 9, 13), (8, 13, 14), (7, 8, 14), (6, 7, 14), (6, 14, 15), (5, 6, 15), (4, 5, 15), (4, 15, 16), (3, 4, 16), (2, 3, 16), (2, 16, 17), (1, 2, 17), (0, 1, 17), (0, 12, 17), (12, 17, 18), (12, 13, 18), (13, 14, 18), (14, 15, 18), (15, 16, 18), (16, 17, 18)]

    POINT_ROAD = [(0, 1), (1, 2, 3), (3, 4), (4, 5), (5, 6, 7), (7, 8), (8, 9, 10), (10, 11), (11, 12), (12, 13, 14), (14, 15), (15, 16, 17), (17, 18), (18, 19), (19, 20, 21), (21, 22), (22, 23, 24), (24, 25), (25, 26), (26, 27, 28), (28, 29), (29, 30, 31), (31, 32), (32, 33), (33, 34, 35), (35, 36), (36, 37, 38), (38, 39), (39, 40), (0, 40, 41), (41, 42, 65), (37, 42, 43), (43, 44, 45), (34, 45, 46), (30, 46, 47), (47, 48, 49), (27, 49, 50), (23, 50, 51), (51, 52, 53), (20, 53, 54), (16, 54, 55), (55, 56, 57), (13, 57, 58), (9, 58, 59), (59, 60, 61), (6, 61, 62), (2, 62, 63), (63, 64, 65), (64, 66, 71), (44, 66, 67), (48, 67, 68), (52, 68, 69), (56, 69, 70), (60, 70, 71)]

    ROAD_POINT = [(0, 29), (0, 1), (1, 46), (1, 2), (2, 3), (3, 4), (4, 45), (4, 5), (5, 6), (6, 43), (6, 7), (7, 8), (8, 9), (9, 42), (9, 10), (10, 11), (11, 40), (11, 12), (12, 13), (13, 14), (14, 39), (14, 15), (15, 16), (16, 37), (16, 17), (17, 18), (18, 19), (19, 36), (19, 20), (20, 21), (21, 34), (21, 22), (22, 23), (23, 24), (24, 33), (24, 25), (25, 26), (26, 31), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (31, 32), (32, 49), (32, 33), (33, 34), (34, 35), (35, 50), (35, 36), (36, 37), (37, 38), (38, 51), (38, 39), (39, 40), (40, 41), (41, 52), (41, 42), (42, 43), (43, 44), (44, 53), (44, 45), (45, 46), (46, 47), (47, 48), (30, 47), (48, 49), (49, 50), (50, 51), (51, 52), (52, 53), (48, 53)]

    PORT_POINT = [(0, 1), (4, 5), (7, 8), (10, 11), (14, 15), (17, 18), (20, 21), (24, 25), (27, 28)]

class Player:
    def __init__(self) -> None:
        self.reset()
    
    def reset(self):
        self.Score = 0
        self.Res_Cards = np.full(5, 0)
        self.ResBank = np.full(5, 0)
        self.Dev_Cards = np.full(5, 0)
        self.Remaining_Roads = 15
        self.Remaining_Settlements = 5
        self.Remaining_Cities = 4
        self.Used_Knight_Cards = 0
        self.Current_Longest_Road_Length = 0
        self.Card_exchange_rate = np.full(5, 4)


class Bank:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.Res_Cards = np.full(5, 15)
        self.ResBank = np.full(5, 4)
        self.Dev_Cards = np.array([14, 2, 2, 2, 5])

class Board:
    def __init__(self) -> None:
        self.reset()
    
    def reset(self):
        self.main_id = 0
        self.Player = [Player() for i in range(4)]
        self.Bank = Bank()

        self.Tile_order = np.array([0, 2, 3]*4 + [1, 4]*3 + [5])
        np.random.shuffle(self.Tile_order)

        self.Robber_location = np.where(self.Tile_order == 5)[0][0]

        self.Prob_order = np.full(19, 0)
        temp = np.ones(19).astype(np.int32)
        temp[self.Robber_location] = 0
        temp_1 = temp.copy()
        for i in range(4):
            tile_idx = np.random.choice(np.where(temp == 1)[0])
            temp[tile_idx] = 0
            temp_1[tile_idx] = 0
            if i < 2:
                self.Prob_order[tile_idx] = 6
            else:
                self.Prob_order[tile_idx] = 8

            for j in CONST.TILE_TILE[tile_idx]:
                temp[j] = 0

        temp = np.array([3, 3, 4, 4, 5, 5, 9, 9, 10, 10, 11, 11, 2, 12])
        np.random.shuffle(temp)
        self.Prob_order[np.where(temp_1 == 1)[0]] = temp

        self.Port_order = np.array([5, 5, 5, 5, 0, 1, 2, 3, 4])
        np.random.shuffle(self.Port_order)

        self.Settlements_and_Cities_state = np.full(54, 0)  # 0,1,2,3,4,5,6,7,8

        self.Roads_state = np.full(72, 0)

        self.Current_Largest_Army = 2
        self.Current_Longest_Road = 4
        self.Current_Largest_Army_idx = 9999
        self.Current_Longest_Road_idx = 9999
    
    def draw_map(self, screen: pygame.Surface):
        screen.fill((50, 150, 200))
        temp_img = pygame.image.load('Image/landing_page_map.png')
        screen.blit(temp_img, (725, 50))

        temp_list = [pygame.transform.smoothscale(pygame.image.load(
            'Image/tile_'+res+'.png'), (133, 152)) for res in RES_NAME+['desert']]
        for i in range(19):
            screen.blit(temp_list[self.Tile_order[i]],
                        (CONST.TILE_CENTER_POS[i][0]-66, CONST.TILE_CENTER_POS[i][1]-76))

        temp_list.clear()

        temp_dict = {i: pygame.transform.smoothscale(pygame.image.load(
            'Image/prob_'+str(i)+'.png'), (55, 55)) for i in range(2, 13) if i != 7}
        for i in range(19):
            if self.Prob_order[i] != 0:
                screen.blit(temp_dict[self.Prob_order[i]], (
                    CONST.TILE_CENTER_POS[i][0]-27, CONST.TILE_CENTER_POS[i][1]-1))

        temp_dict.clear()

        temp = []
        port_pier = pygame.transform.smoothscale(
            pygame.image.load('Image/port_pier.png'), (15, 52))
        temp.append(port_pier)
        temp.append(pygame.transform.rotate(port_pier, 60))
        temp.append(pygame.transform.rotate(port_pier, 120))
        port_pier_pos = [[(904, 115), (1186, 115), (1397, 236), (1397, 617), (1186, 739), (904, 739)], [(929, 96), (1475, 408), (
            1334, 651), (1122, 771), (789, 580), (789, 337)], [(1122, 96), (1334, 217), (1475, 460), (929, 771), (789, 530), (789, 287)]]
        
        for i in range(3):
            for pos in port_pier_pos[i]:
                screen.blit(temp[i], pos)

        port_topleft_pos = [(1146, 31), (1357, 153), (1499, 396), (1357, 639),
                            (1146, 759), (864, 758), (724, 517), (724, 274), (864, 31)]
        temp_list = [pygame.transform.smoothscale(pygame.image.load(
            'Image/port_'+res+'.png'), (80, 80)) for res in RES_NAME]
        temp_list.append(pygame.transform.smoothscale(
            pygame.image.load('Image/port.png'), (80, 80)))
        for i in range(9):
            screen.blit(temp_list[self.Port_order[i]], port_topleft_pos[i])

        temp_list.clear()

        return screen.copy()
    
def convert_env_to_board(env: np.ndarray):
    BOARD = Board()

    # Thứ tự mảnh ghép
    BOARD.Tile_order = env[0:19].astype(int)
    temp = RES_NAME + ['Desert']
    print('Tile:', [temp[i] for i in BOARD.Tile_order])

    #
    BOARD.Robber_location = int(env[19])
    print('Robbber pos:', BOARD.Robber_location)

    #
    BOARD.Prob_order = env[20:39].astype(int)
    print('Prob:', BOARD.Prob_order)

    #
    BOARD.Port_order = env[39:48].astype(int)
    temp = RES_NAME + ['3:1 port']
    print('Port:', [temp[i] for i in BOARD.Port_order])

    return BOARD


class Dynamic_Sprite(pygame.sprite.Sprite):
    def __init__(self, image, pos, align='center'):
        super().__init__()
        self.pos = list(pos)
        self.align = align
        self.set_image(image)

        self.is_moving = False
        self.current_step = 0
        self.amount_step = 0
        self.des_pos = [0, 0]
        self.old_pos = [0, 0]

    def set_image(self, image):
        self.image = image
        self.rect = image.get_rect()
        setattr(self.rect, self.align, self.pos)

    def copy(self):
        return Dynamic_Sprite(self.image, self.pos, self.align)

    def move(self, des_pos, align, amount_step):
        self.is_moving = True
        self.current_step = 0
        self.amount_step = amount_step
        self.old_pos = self.pos.copy()
        for i in range(2):
            self.des_pos[i] = des_pos[i] - \
                getattr(self.rect, align)[i] + self.old_pos[i]

    def update(self):
        if self.is_moving:
            self.current_step += 1
            for i in range(2):
                self.pos[i] = (self.des_pos[i] - self.old_pos[i]) / \
                    self.amount_step * self.current_step + self.old_pos[i]

            setattr(self.rect, self.align, self.pos)

            if self.current_step >= self.amount_step:
                self.is_moving = False

    def set_pos(self, pos):
        self.pos = list(pos)
        setattr(self.rect, self.align, self.pos)


_circle_cache = {}


def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]

    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1

    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render_outline(text, font, font_color):
    o_color = (255-font_color[0], 255-font_color[1], 255-font_color[2])
    opx = 1

    text_surface = font.render(text, True, font_color).convert_alpha()
    w = text_surface.get_width() + 2*opx
    h = font.get_height()

    o_surf = pygame.Surface((w, h+2*opx)).convert_alpha()
    o_surf.fill((0, 0, 0, 0))
    surf = o_surf.copy()
    o_surf.blit(font.render(text, True, o_color).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(o_surf, (dx+opx, dy+opx))

    surf.blit(text_surface, (opx, opx))
    return surf


class TextRectException:
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


def multiline_surface(text, font_size=36, font_color=RGB_color.SPRING_GREEN, rect_size=(700, 120), align='center'):
    rect = pygame.rect.Rect(0, 0, rect_size[0], rect_size[1])
    font = pygame.font.Font('freesansbold.ttf', font_size)

    final_lines = []
    requested_lines = text.splitlines()
    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException(
                        "The word " + word + " is too long to fit in the rect passed.")

            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "

            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    surface = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
    surface = surface.convert_alpha()

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException(
                "Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            temp_surface = render_outline(line, font, font_color)
        if align == 'left':
            surface.blit(temp_surface, (0, accumulated_height))
        elif align == 'center':
            surface.blit(
                temp_surface, ((rect.width - temp_surface.get_width()) / 2, accumulated_height))
        elif align == 'right':
            surface.blit(temp_surface, (rect.width -
                         temp_surface.get_width(), accumulated_height))
        else:
            raise TextRectException("Invalid align argument: " + str(align))

        accumulated_height += font.size(line)[1]
    return surface


class Static_Sprite(pygame.sprite.Sprite):
    def __init__(self, value, font_size, font_color, pos, align='center'):
        super().__init__()
        font = pygame.font.Font('freesansbold.ttf', font_size)

        self.font_color = font_color
        self.pos = list(pos)
        self.align = align
        self.font = font
        self.set_value(value)

    def set_value(self, value):
        self.image = render_outline(str(value), self.font, self.font_color)
        self.rect = self.image.get_rect()
        setattr(self.rect, self.align, self.pos)
        self.value = value

    def change_color(self, font_color):
        self.image = render_outline(str(self.value), self.font, font_color)
        self.font_color = font_color


class Player_sprite:
    def __init__(self, name, p_idx):
        self.Name = Static_Sprite(
            name, 28, RGB_color.SPRING_GREEN, (80, 305+150*p_idx), 'midtop')
        
        self.Score = Static_Sprite(
            '0 (0)', 28, RGB_color.SPRING_GREEN, (80, 335+150*p_idx), 'midtop')
        
        self.Icon_largest_army = Dynamic_Sprite(
            Image.Largest_army, (55, 380+150*p_idx), 'midtop')
        self.Icon_longest_road = Dynamic_Sprite(
            Image.Longest_road, (105, 380+150*p_idx), 'midtop')
        self.Amount_used_knight = Static_Sprite(
            0, 20, RGB_color.BLACK, (55, 420+150*p_idx), 'midtop')
        self.Current_longest_road_length = Static_Sprite(
            0, 20, RGB_color.BLACK, (105, 420+150*p_idx), 'midtop')

        self.Res_Cards = []
        self.ResBank = []
        self.Number_Res_Cards = []
        self.Number_ResBank = []

        self.Dev_Cards = []
        self.Number_Dev_Cards = []
        k = 0
        for i in range(5):
            self.Res_Cards.append(Dynamic_Sprite(
                Image.Res_card[i], (160+50*k, 305+150*p_idx), 'topleft'))
            self.ResBank.append(Dynamic_Sprite(
                Image.Res_card[i], (430+50*k, 305+150*p_idx), 'topleft'))
            self.Number_Res_Cards.append(Static_Sprite(
                0, 20, RGB_color.BLACK, (200+50*k, 365+150*p_idx), 'bottomright'))
            self.Number_ResBank.append(Static_Sprite(
                0, 20, RGB_color.BLACK, (470+50*k, 365+150*p_idx), 'bottomright'))
            
            self.Dev_Cards.append(Dynamic_Sprite(
                Image.Dev_card[i], (160+50*k, 380+150*p_idx), 'topleft'))
            self.Number_Dev_Cards.append(Static_Sprite(
                0, 20, RGB_color.BLACK, (200+50*k, 440+150*p_idx), 'bottomright'))
            k += 1


class Bank_sprite:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.Res_Cards = []
        self.Number_ResBank = []
        self.Number_Res_Cards = []
        k = 0
        for i in range(5):
            self.Res_Cards.append(Dynamic_Sprite(
                Image.Res_card[i], (160+50*k, 210), 'topleft'))
            self.Number_Res_Cards.append(Static_Sprite(
                15, 20, RGB_color.BLACK, (200+50*k, 270), 'bottomright'))
            self.Number_ResBank.append(Static_Sprite(
                4, 20, RGB_color.BLACK, (200+50*k, 235), 'bottomright'))
            k += 1

        self.Dev_Cards = Dynamic_Sprite(
            Image.Dev_card[5], (410, 210), 'topleft')
        self.Number_Dev_Cards = Static_Sprite(
            25, 20, RGB_color.BLACK, (450, 270), 'bottomright')


class Sprite:
    def __init__(self, list_player_name) -> None:
        self.reset(list_player_name)
    
    def reset(self, list_player_name):
        self.Robber = Dynamic_Sprite(Image.Robber, (-999, -999), 'midright')
        self.Notification = Dynamic_Sprite(multiline_surface(
            'Welcome to The Settlers of Catan!'), (0, 15), 'topleft')
        self.Player = [Player_sprite(list_player_name[i], i) for i in range(4)]
        self.Bank = Bank_sprite()
        self.Settlements_and_Cities = [Dynamic_Sprite(pygame.Surface(
            (30, 30)), CONST.POINT_COORDINATE[i], 'center') for i in range(54)]
        
        self.Dices = [Dynamic_Sprite(pygame.Surface(
            (60, 60)), (477+67*i, 210), 'topleft') for i in range(2)]
        
        self.Point_highlight_circle = [Dynamic_Sprite(
            Image.Small_highlight_circle, CONST.POINT_COORDINATE[i], 'center') for i in range(54)]

        self.Road_highlight_circle = [Dynamic_Sprite(
            Image.Small_highlight_circle, CONST.ROAD_CENTER_POS[i], 'center') for i in range(72)]

        self.Tile_highlight_circle = [Dynamic_Sprite(
            Image.Big_highlight_circle, CONST.TILE_CENTER_POS[i], 'center') for i in range(19)]

def compare_numba_graphic(board: Board, env):
    check = False
    if env[244] != board.main_id:
        print('Khác id người chơi', env[244], board.main_id)
        check = True
    
    for i in range(4):
        s_ = 58 + 42*i
        if (env[s_:s_+5] != board.Player[i].Res_Cards).any():
            print('Khác tài nguyên người chơi', i, ': ', env[s_:s_+5], board.Player[i].Res_Cards)
            check = True

        if (env[s_+5:s_+10] != board.Player[i].Dev_Cards).any():
            print('Khác thẻ dev người chơi', i, ': ', env[s_+5:s_+10], board.Player[i].Dev_Cards)
            check = True
        
        if env[s_+35] != board.Player[i].Used_Knight_Cards:
            print('Khác số thẻ knight đã dùng người chơi', i, env[s_+35], board.Player[i].Used_Knight_Cards)
            check = True
        
        if env[s_+36] != board.Player[i].Current_Longest_Road_Length:
            print('Khác con đường dài nhất người chơi', i, env[s_+36], board.Player[i].Current_Longest_Road_Length)
            check = True
        
        if env[s_+10] != board.Player[i].Score:
            print('Khác điểm người chơi', i, env[s_+10], board.Player[i].Score)
            check = True

    if board.Current_Largest_Army_idx != env[226]:
        if board.Current_Largest_Army_idx == 9999 and env[226] == -1:
            pass
        else:
            print(env)
            print(f'sai người chơi nhiều knight nhất(giá trị range(0,4))')
            check = True
    
    if board.Current_Longest_Road_idx != env[227]:
        if board.Current_Longest_Road_idx == 9999 and env[227] == -1:
            pass
        else:
            print(env)
            print(f'sai người chơi nhiều knight nhất(giá trị range(0,4))', env[227], board.Current_Largest_Army_idx)
            check = True
    
    if board.Robber_location != env[19]:
        print(env)
        print('sai vị trí của robber(giá trị range(0,19))', board.Robber_location, env[19])
        check = True
    
    if check:
        print(env[228])
        input('Saiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    
    return True



