import pygame
import sys
import random
import numpy
from Catan import *
import env

def random_player(p_state, temp_file, per_file):
    arr_action = env.getValidActions(p_state)
    arr_action = np.where(arr_action == 1)[0]
    action = np.random.choice(arr_action)
    print('Arr', arr_action, 'action', action, np.where(p_state[205:218]==1)[0])
    return action, temp_file, per_file

from env import ROAD_PRICE, CITY_PRICE, SETTLEMENT_PRICE, DEV_PRICE as DEV_CARD_PRICE

# Import
list_player_name = ['Mysticblue', 'Gold', 'Silver', 'Bronze']
list_player_type = ['B', 'B', 'B', 'B']
list_player_color = ['mysticblue', 'gold', 'silver', 'bronze']
list_player = [random_player, random_player, random_player, random_player]

SPEED = 10000

# Đừng chỉnh gì ở dưới đây

SPEED_1 = 1.0
if SPEED > 5:
    SPEED_1 = SPEED/5
    SPEED = 5

temp = [0, 1, 2, 3]
random.shuffle(temp)
list_player_name = [list_player_name[i] for i in temp]
list_player_type = [list_player_type[i] for i in temp]
list_player_color = [list_player_color[i] for i in temp]
list_player = [list_player[i] for i in temp]

Image.set_color(list_player_color)

env_state = env.initEnv()

BOARD = convert_env_to_board(env_state)
SPRITE = Sprite(list_player_name)

# Tạo màn hình
pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()

layer_0 = pygame.sprite.Group()  # Lớp dưới cùng
layer_1 = pygame.sprite.Group()  # Lớp dưới cùng
layer_2 = pygame.sprite.Group()  # Settlement and Citites
layer_3 = pygame.sprite.Group()  # Lớp cho những thứ chuyển động
layer_4 = pygame.sprite.Group()  # Lớp trên cùng (pause game)

background = BOARD.draw_map(screen)

# Đặt Robber
layer_0.add(SPRITE.Robber)
SPRITE.Robber.set_pos(CONST.TILE_CENTER_POS[BOARD.Robber_location])

# Thông báo
layer_0.add(SPRITE.Notification)

#
for p_idx in range(4):
    layer_0.add(SPRITE.Player[p_idx].Name)
    layer_0.add(SPRITE.Player[p_idx].Score)
    layer_0.add(SPRITE.Player[p_idx].ResBank)
    layer_0.add(SPRITE.Player[p_idx].Number_ResBank)


#
layer_0.add(SPRITE.Bank.Res_Cards)
layer_0.add(SPRITE.Bank.Number_ResBank)
layer_0.add(SPRITE.Bank.Number_Res_Cards)

for p_idx in range(4):
    layer_0.add(SPRITE.Player[p_idx].Res_Cards)
    layer_0.add(SPRITE.Player[p_idx].Number_Res_Cards)
    layer_0.add(SPRITE.Player[p_idx].Dev_Cards)
    layer_0.add(SPRITE.Player[p_idx].Number_Dev_Cards)

layer_0.add(SPRITE.Bank.Dev_Cards)
layer_0.add(SPRITE.Bank.Number_Dev_Cards)

#
for p_idx in range(4):
    layer_0.add(SPRITE.Player[p_idx].Icon_largest_army)
    layer_0.add(SPRITE.Player[p_idx].Icon_longest_road)
    layer_0.add(SPRITE.Player[p_idx].Amount_used_knight)
    layer_0.add(SPRITE.Player[p_idx].Current_longest_road_length)


###########################################################################

def _(k):
    return round(k/SPEED_1)

def update_display(move):
    screen.blit(background, (0, 0))
    layer_0.draw(screen)
    layer_1.draw(screen)
    layer_2.draw(screen)
    layer_3.draw(screen)
    layer_4.draw(screen)

    if move:
        layer_3.update()

    pygame.display.flip()

    if move:
        clock.tick(60*SPEED)
    else:
        clock.tick(60)

def pause_game():
    temp = Dynamic_Sprite(multiline_surface(
        'GAME PAUSED', font_size=72, rect_size=(800, 450)), (800, 450), 'center')
    layer_4.add(temp)
    is_Running = True
    while is_Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_Running = False

        update_display(move=False)

    layer_4.empty()

def check_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        pause_game()
        return True

    return False

def hold_display(times, move):
    k = 0
    while k < times:
        for event in pygame.event.get():
            if check_event(event):
                break

        update_display(move=move)
        k += 1
    
###########################################################################
def change_player_name_color(p_idx, color):
    SPRITE.Player[p_idx].Name.change_color(color)
    SPRITE.Player[p_idx].Score.change_color(color)

def set_notification(text):
    SPRITE.Notification.set_image(multiline_surface(text))

def datNha(p_idx, list_diemCoTheDat):
    list_diemCoTheDat = list(np.where(env.getValidActions(env.getAgentState(env_state))==1)[0])
    for diem in list_diemCoTheDat:
        layer_3.add(SPRITE.Point_highlight_circle[diem])
    
    hold_display(_(60), False)

    
    ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
    diemDatNha, tf, pf = random_player(env.getAgentState(env_state), [0], [0])

    env.stepEnv(env_state, diemDatNha)

    layer_3.empty()

    BOARD.Settlements_and_Cities_state[diemDatNha] = p_idx+1
    BOARD.Player[p_idx].Remaining_Settlements -= 1
    ANIMATION.datNha(diemDatNha, p_idx, 0)
    BOARD.Player[p_idx].Score += 1
    SPRITE.Player[p_idx].Score.set_value(
        f'{BOARD.Player[p_idx].Score} ({BOARD.Player[p_idx].Dev_Cards[4]})')
    for port_idx in range(9):
        if diemDatNha in CONST.PORT_POINT[port_idx]:
            if BOARD.Port_order[port_idx] == 5:
                BOARD.Player[p_idx].Card_exchange_rate = numpy.minimum(
                    BOARD.Player[p_idx].Card_exchange_rate, numpy.full(5, 3))
            else:
                BOARD.Player[p_idx].Card_exchange_rate[BOARD.Port_order[port_idx]] = 2

            break
    
    return diemDatNha

def datDuong(p_idx, list_DuongCoTheDat):
    for diem in list_DuongCoTheDat:
        layer_3.add(SPRITE.Road_highlight_circle[diem])
    
    hold_display(_(60), False)

    ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
    
    duongDuocChon = 9999999
    diem_t1 = int(env_state[231])
    diem_t2, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
    layer_3.empty()

    env.stepEnv(env_state, diem_t2)
    for road_idx in range(72):
        if diem_t1 in CONST.ROAD_POINT[road_idx] and diem_t2 in CONST.ROAD_POINT[road_idx]:
            duongDuocChon = road_idx
            break
    
    if duongDuocChon == 999999:
        print(diem_t1, diem_t2)
        input('HGDYSG')
    

    BOARD.Roads_state[duongDuocChon] = p_idx + 1
    BOARD.Player[p_idx].Remaining_Roads -= 1
    ANIMATION.datDuong(duongDuocChon, p_idx)

    longest_road_player = CHECK.conDuongDaiNhat_1(p_idx)
    BOARD.Player[p_idx].Current_Longest_Road_Length = longest_road_player
    SPRITE.Player[p_idx].Current_longest_road_length.set_value(
        longest_road_player)

def datDuongGiuaGame(p_idx, list_DuongCoTheDat):
    for diem in list_DuongCoTheDat:
        layer_3.add(SPRITE.Road_highlight_circle[diem])
    
    hold_display(_(60), False)
    ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
    diem_t1, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
    env.stepEnv(env_state, diem_t1)
    diem_t2, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
    env.stepEnv(env_state, diem_t2)
    layer_3.empty()

    print(diem_t1, diem_t2)

    for road_idx in range(72):
        if diem_t1 in CONST.ROAD_POINT[road_idx] and diem_t2 in CONST.ROAD_POINT[road_idx]:
            duongDuocChon = road_idx
            break
    
    BOARD.Roads_state[duongDuocChon] = p_idx + 1
    BOARD.Player[p_idx].Remaining_Roads -= 1
    ANIMATION.datDuong(duongDuocChon, p_idx)

    longest_road_player = CHECK.conDuongDaiNhat_1(p_idx)
    BOARD.Player[p_idx].Current_Longest_Road_Length = longest_road_player
    SPRITE.Player[p_idx].Current_longest_road_length.set_value(
        longest_road_player)

def datThanhPho(p_idx, list_diemCoTheDat):

    for diem in list_diemCoTheDat:
        layer_3.add(SPRITE.Point_highlight_circle[diem])

    ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
    diemDatNha, tf, pf = random_player(env.getAgentState(env_state), [0], [0])

    env.stepEnv(env_state, diemDatNha)

    # print('Điểm đặt nhà:', diemDatNha)
    BOARD.Settlements_and_Cities_state[diemDatNha] = -p_idx-1
    BOARD.Player[p_idx].Remaining_Cities -= 1
    BOARD.Player[p_idx].Remaining_Settlements += 1
    ANIMATION.datNha(diemDatNha, p_idx, 1)
    BOARD.Player[p_idx].Score += 1
    SPRITE.Player[p_idx].Score.set_value(
        f'{BOARD.Player[p_idx].Score} ({BOARD.Player[p_idx].Dev_Cards[4]})')

    return diemDatNha

def diChuyenRobber(p_idx):
    list_DiemCoTheDat = list(np.where(env.getValidActions(env.getAgentState(env_state))==1)[0])

    for diem in list_DiemCoTheDat:
        layer_3.add(SPRITE.Tile_highlight_circle[diem-64])

    hold_display(_(60), False)

    ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
    new_Robber_pos_numba, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
    new_Robber_pos = new_Robber_pos_numba - 64 # Dịch sang [0:18]

    layer_3.empty()

    env.stepEnv(env_state, new_Robber_pos_numba)
    ANIMATION.Robber_move(new_Robber_pos)
    BOARD.Robber_location = new_Robber_pos
    if BOARD.Tile_order[new_Robber_pos] != 5 and BOARD.Bank.Res_Cards[BOARD.Tile_order[new_Robber_pos]] > 0:
        list_tile_nearest = [new_Robber_pos]
    else:
        list_tile_nearest = []
    list_TnNhan = numpy.full(19, 0)
    list_TnNhan[list_tile_nearest] = 1
    list_res_reci, list_res_str = ANIMATION.nhanTaiNguyenTuMap(
        list_TnNhan, p_idx)
    for res_idx in range(5):
        if list_res_reci[res_idx] > 0:
            BOARD.Bank.Res_Cards[res_idx] -= list_res_reci[res_idx]
            BOARD.Player[p_idx].Res_Cards[res_idx] += list_res_reci[res_idx]
            SPRITE.Bank.Number_Res_Cards[res_idx].set_value(
                BOARD.Bank.Res_Cards[res_idx])
            SPRITE.Player[p_idx].Number_Res_Cards[res_idx].set_value(
                BOARD.Player[p_idx].Res_Cards[res_idx])

    set_notification(
        list_player_name[p_idx] + ' got: ' + str(list_res_str))
    hold_display(_(60), False)

def traNhieuTN(p_idx, list_res_idx):
    for res_idx in list_res_idx:
        BOARD.Player[p_idx].Res_Cards[res_idx] -= 1
        SPRITE.Player[p_idx].Number_Res_Cards[res_idx].set_value(
            BOARD.Player[p_idx].Res_Cards[res_idx])
        ANIMATION.traTaiNguyenBank(p_idx, res_idx)
        BOARD.Bank.Res_Cards[res_idx] += 1
        SPRITE.Bank.Number_Res_Cards[res_idx].set_value(
            BOARD.Bank.Res_Cards[res_idx])

def check_win():
    list_score = []
    for p_idx in range(4):
        list_score.append(
            BOARD.Player[p_idx].Score + BOARD.Player[p_idx].Dev_Cards[4])

    max_score = max(list_score)
    if max_score >= 10:
        for i in range(3, -1, -1):
            if list_score[i] == max_score:
                set_notification(
                    'Congratulation! ' + list_player_name[i] + ' win this freeking Game!')
                hold_display(999999, False)

def check_longest_Road():
    list_p_longest_Road = []
    for p_idx in range(4):
        l_ = CHECK.conDuongDaiNhat_1(p_idx)
        list_p_longest_Road.append(l_)
        BOARD.Player[p_idx].Current_Longest_Road_Length = l_
        SPRITE.Player[p_idx].Current_longest_road_length.set_value(
            BOARD.Player[p_idx].Current_Longest_Road_Length)

    longgest_length = max(list_p_longest_Road)
    if longgest_length < 5:
        if BOARD.Current_Longest_Road_idx == 9999:  # Chưa có ông nào có danh hiệu
            pass
        else:  # Có ông có danh hiệu nhưng vừa bị cướp con đường dài nhất
            old_p_idx = BOARD.Current_Longest_Road_idx
            BOARD.Current_Longest_Road_idx = 9999
            BOARD.Current_Longest_Road = longgest_length
            BOARD.Player[old_p_idx].Score -= 2  # Trừ điểm thằng cũ
            SPRITE.Player[old_p_idx].Score.set_value(
                f'{BOARD.Player[old_p_idx].Score} ({BOARD.Player[old_p_idx].Dev_Cards[4]})')
            SPRITE.Player[old_p_idx].Icon_longest_road.set_image(
                Image.Longest_road)
    else:
        list_p_longest = []
        for i in range(4):
            if list_p_longest_Road[i] == longgest_length:
                list_p_longest.append(i)

        if len(list_p_longest) == 1:  # Có đúng 1 ông dài nhất
            if BOARD.Current_Longest_Road_idx == 9999:  # Chưa có ai có longest road, ghi nhận danh hiệu cho ông này
                # Bàn chơi ghi nhận
                BOARD.Current_Longest_Road_idx = list_p_longest[0]
                BOARD.Current_Longest_Road = longgest_length  # Bàn chơi ghi nhận
                BOARD.Player[list_p_longest[0]].Score += 2  # Cộng điểm
                SPRITE.Player[list_p_longest[0]].Score.set_value(
                    f'{BOARD.Player[list_p_longest[0]].Score} ({BOARD.Player[list_p_longest[0]].Dev_Cards[4]})')  # Cập nhật lên màn hình
                SPRITE.Player[list_p_longest[0]].Icon_longest_road.set_image(
                    Image.Longest_road_highlight)  # Cập nhật highlight
            else:  # Đã có longest_road
                # Cùng người, không thay đổi gì
                if BOARD.Current_Longest_Road_idx == list_p_longest[0]:
                    BOARD.Current_Longest_Road = longgest_length
                else:  # Khác người, đổi danh hiệu cho ông mới, trừ điểm ông cũ
                    old_p_idx = BOARD.Current_Longest_Road_idx
                    # Bàn chơi ghi nhận
                    BOARD.Current_Longest_Road_idx = list_p_longest[0]
                    BOARD.Current_Longest_Road = longgest_length  # Bàn chơi ghi nhận
                    # Cộng điểm thằng mới
                    BOARD.Player[list_p_longest[0]].Score += 2
                    SPRITE.Player[list_p_longest[0]].Score.set_value(
                        f'{BOARD.Player[list_p_longest[0]].Score} ({BOARD.Player[list_p_longest[0]].Dev_Cards[4]})')
                    BOARD.Player[old_p_idx].Score -= 2  # Trừ điểm thằng cũ
                    SPRITE.Player[old_p_idx].Score.set_value(
                        f'{BOARD.Player[old_p_idx].Score} ({BOARD.Player[old_p_idx].Dev_Cards[4]})')
                    SPRITE.Player[list_p_longest[0]].Icon_longest_road.set_image(
                        Image.Longest_road_highlight)  # Highlight
                    SPRITE.Player[old_p_idx].Icon_longest_road.set_image(
                        Image.Longest_road)
        else:  # Có 2 trở lên người cùng có con đường dài nhất
            if BOARD.Current_Longest_Road_idx in list_p_longest:  # Một trong số 2 người này đang sở hữu danh hiệu
                BOARD.Current_Longest_Road = longgest_length
            else:  # tất cả người có con đường dài nhất đều không nắm giữ danh hiệu
                if BOARD.Current_Longest_Road_idx == 9999:  # Chưa có ai có danh hiệu
                    pass
                else:  # Đang có, tức là ông đang nắm giữu bị cướp con đường dài nhất, cần thu hồi lại
                    old_p_idx = BOARD.Current_Longest_Road_idx
                    BOARD.Current_Longest_Road_idx = 9999
                    BOARD.Current_Longest_Road = longgest_length
                    BOARD.Player[old_p_idx].Score -= 2  # Trừ điểm thằng cũ
                    SPRITE.Player[old_p_idx].Score.set_value(
                        f'{BOARD.Player[old_p_idx].Score} ({BOARD.Player[old_p_idx].Dev_Cards[4]})')
                    SPRITE.Player[old_p_idx].Icon_longest_road.set_image(
                        Image.Longest_road)

def check_largest_Army(p_idx):
    if BOARD.Current_Largest_Army_idx == p_idx:
        BOARD.Current_Largest_Army = BOARD.Player[p_idx].Used_Knight_Cards
    else:
        if BOARD.Player[p_idx].Used_Knight_Cards > BOARD.Current_Largest_Army:  # Lớn hơn
            print(BOARD.Player[p_idx].Used_Knight_Cards,BOARD.Current_Largest_Army, 'muahahahahahahahahaha')

            old_p_idx = BOARD.Current_Largest_Army_idx
            if old_p_idx != 9999:
                BOARD.Player[old_p_idx].Score -= 2

            BOARD.Player[p_idx].Score += 2
            if old_p_idx != 9999:
                SPRITE.Player[old_p_idx].Score.set_value(
                    f'{BOARD.Player[old_p_idx].Score} ({BOARD.Player[old_p_idx].Dev_Cards[4]})')

            SPRITE.Player[p_idx].Score.set_value(
                f'{BOARD.Player[p_idx].Score} ({BOARD.Player[p_idx].Dev_Cards[4]})')

            BOARD.Current_Largest_Army_idx = p_idx
            BOARD.Current_Largest_Army = BOARD.Player[p_idx].Used_Knight_Cards
            SPRITE.Player[p_idx].Icon_largest_army.set_image(
                Image.Largest_army_highlight)
            if old_p_idx != 9999:
                SPRITE.Player[old_p_idx].Icon_largest_army.set_image(
                    Image.Largest_army)


###########################################################################
class Check:
    def __init__(self) -> None:
        pass

    def conDuongDaiNhat_1(self, p_idx):
        def find_max(length, diem_Xp, list_duongDaDi, p_roads, p_points) -> int:
            list_duongCheck = []
            for road in CONST.POINT_ROAD[diem_Xp]:
                if road in p_roads and road not in list_duongDaDi:
                    list_duongCheck.append(road)

            if len(list_duongCheck) == 0 or diem_Xp not in p_points:
                if length != 0:
                    return length

            max_length = length
            for road in list_duongCheck:
                list_duongDaDi_copy = list_duongDaDi.copy()
                list_duongDaDi_copy.append(road)

                diem_Xp_1 = 9999
                for diem in CONST.ROAD_POINT[road]:
                    if diem != diem_Xp:
                        diem_Xp_1 = diem
                        break

                length_1 = find_max(length+1, diem_Xp_1,
                                    list_duongDaDi_copy, p_roads, p_points)
                if length_1 > max_length:
                    max_length = length_1

            return max_length

        p_roads = [i for i in range(72) if BOARD.Roads_state[i] == p_idx+1]
        p_points = []
        for road in p_roads:
            for point in CONST.ROAD_POINT[road]:
                if BOARD.Settlements_and_Cities_state[point] in [0, p_idx+1, -p_idx-1] and point not in p_points:
                    p_points.append(point)

        full_point = []
        for road in p_roads:
            for point in CONST.ROAD_POINT[road]:
                if point not in full_point:
                    full_point.append(point)

        max_length = 0
        for point in full_point:
            length = find_max(0, point, [], p_roads, p_points)
            if length > max_length:
                max_length = length

        return max_length

    def listActionDauMoiTurn(self, p_idx):
        list_action = ['roll_dice']
        if BOARD.Player[p_idx].Dev_Cards[0] > 0:
            list_action.append('knight')

        if BOARD.Player[p_idx].Dev_Cards[1] > 0 and self.viTriXayDuong(p_idx)[0]:
            list_action.append('roadbuilding')

        if BOARD.Player[p_idx].Dev_Cards[2] > 0 and sum(BOARD.Bank.Res_Cards) > 0:
            list_action.append('yearofplenty')

        if BOARD.Player[p_idx].Dev_Cards[3] > 0:
            list_action.append('monopoly')
        
        return list_action
    

    def soLuongTaiNguyenTraDo7(self, main_p_idx):
        list_num_return = []
        for i in range(4):
            p_idx = (main_p_idx + i) % 4
            if sum(BOARD.Player[p_idx].Res_Cards) > 7:
                list_num_return.append(
                    int(sum(BOARD.Player[p_idx].Res_Cards)/2.0))
            else:
                list_num_return.append(0)

        return list_num_return
    
    def viTriXayDuong(self, p_idx):
        if BOARD.Player[p_idx].Remaining_Roads == 0:
            return False, []

        p_roads = [i for i in range(72) if BOARD.Roads_state[i] == p_idx+1]
        p_points = []
        for road in p_roads:
            for point in CONST.ROAD_POINT[road]:
                if BOARD.Settlements_and_Cities_state[point] in [0, p_idx+1, -p_idx-1] and point not in p_points:
                    p_points.append(point)

        list_road_can_build = []
        for point in p_points:
            for road in CONST.POINT_ROAD[point]:
                if BOARD.Roads_state[road] == 0:
                    list_road_can_build.append(road)

        if len(list_road_can_build) > 0:
            return True, list_road_can_build

        return False, []

    def khaNangXayDuong(self, p_idx):
        if (BOARD.Player[p_idx].Res_Cards < ROAD_PRICE).any():
            return False, []

        return self.viTriXayDuong(p_idx)

    def khaNangXayNha(self, p_idx):
        if (BOARD.Player[p_idx].Res_Cards < SETTLEMENT_PRICE).any():
            return False, []

        if BOARD.Player[p_idx].Remaining_Settlements == 0:
            return False, []

        p_roads = numpy.where(BOARD.Roads_state == (p_idx+1))[0]
        p_points = []
        for road in p_roads:
            for point in CONST.ROAD_POINT[road]:
                if BOARD.Settlements_and_Cities_state[point] == 0 and point not in p_points:
                    p_points.append(point)

        list_point_can_build = []
        for point in p_points:
            check = True
            for point_1 in CONST.POINT_POINT[point]:
                if BOARD.Settlements_and_Cities_state[point_1] != 0:
                    check = False
                    break
                else:
                    continue

            if check:
                list_point_can_build.append(point)

        if len(list_point_can_build) > 0:
            return True, list_point_can_build
        else:
            return False, []

    def khaNangXayThanhPho(self, p_idx):
        if (BOARD.Player[p_idx].Res_Cards < CITY_PRICE).any():
            return False, []

        if BOARD.Player[p_idx].Remaining_Cities == 0:
            return False, []

        if BOARD.Player[p_idx].Remaining_Settlements < 5:
            list_point_can_buid = [i for i in range(
                54) if BOARD.Settlements_and_Cities_state[i] == p_idx+1]
            return True, list_point_can_buid

        return False, []

    def khaNangMuaDev(self, p_idx):
        if (BOARD.Player[p_idx].Res_Cards < DEV_CARD_PRICE).any():
            return False

        if np.sum(BOARD.Bank.Dev_Cards) == 0:
            return False

        return True


    def actionCoTheLam(self, p_idx, list_action: list, layTNtuKho):
        # Xây đường
        if self.khaNangXayDuong(p_idx)[0]:
            if 'build_road' not in list_action:
                list_action.append('build_road')
        else:
            if 'build_road' in list_action:
                list_action.remove('build_road')

        # Xây nhà
        if self.khaNangXayNha(p_idx)[0]:
            if 'build_settlement' not in list_action:
                list_action.append('build_settlement')
        else:
            if 'build_settlement' in list_action:
                list_action.remove('build_settlement')

        # Xây thành phố
        if self.khaNangXayThanhPho(p_idx)[0]:
            if 'build_city' not in list_action:
                list_action.append('build_city')
        else:
            if 'build_city' in list_action:
                list_action.remove('build_city')

        # Mua thẻ dev
        if self.khaNangMuaDev(p_idx):
            if 'buy_dev' not in list_action:
                list_action.append('buy_dev')
        else:
            if 'buy_dev' in list_action:
                list_action.remove('buy_dev')
        
        # Trade bank
        check_trade_bank = False
        for res_idx in range(5):
            if BOARD.Player[p_idx].Res_Cards[res_idx] >= BOARD.Player[p_idx].Card_exchange_rate[res_idx]:
                for res_idx_1 in range(5):
                    if res_idx_1 != res_idx and BOARD.Bank.Res_Cards[res_idx_1] > 0:
                        check_trade_bank = True
                        break

                if check_trade_bank:
                    break

        if check_trade_bank:
            if 'trade_bank' not in list_action:
                list_action.append('trade_bank')
        else:
            if 'trade_bank' in list_action:
                list_action.remove('trade_bank')
        
        if layTaiNguyenTuKho:
            if 'take_res_from_storage' not in list_action:
                list_action.append('take_res_from_storage')
        else:
            if 'take_res_from_storage' in list_action:
                list_action.remove('take_res_from_storage')
        
        return list_action


CHECK = Check()


class Animation:
    def __init__(self) -> None:
        pass

    def datNha(self, diemDat, p_idx, loaiNha):
        '''
        loaiNha: 0 -> Settlement, 1 -> City
        '''
        temp = SPRITE.Settlements_and_Cities[diemDat].copy()
        if loaiNha == 0:
            temp.set_image(Image.Settlements[p_idx])
        else:
            temp.set_image(Image.Cities[p_idx])

        des = temp.rect.center
        temp.set_pos((des[0], des[1]-150))
        layer_3.add(temp)
        temp.move(des, 'center', _(60))
        hold_display(_(60), move=True)
        layer_3.empty()
        SPRITE.Settlements_and_Cities[diemDat].set_image(temp.image)
        layer_2.add(SPRITE.Settlements_and_Cities[diemDat])
    
    def datDuong(self, duongDuocChon, p_idx):
        pos_1 = CONST.POINT_COORDINATE[CONST.ROAD_POINT[duongDuocChon][0]]
        pos_2 = CONST.POINT_COORDINATE[CONST.ROAD_POINT[duongDuocChon][1]]
        x = pos_1[0] - pos_2[0]
        y = pos_1[1] - pos_2[1]
        z = x*y

        img = None
        if z == 0:
            img = Image.Roads[p_idx]
        elif z > 0:
            img = pygame.transform.rotate(Image.Roads[p_idx], 60)
        else:
            img = pygame.transform.rotate(Image.Roads[p_idx], 120)

        road_pos = CONST.ROAD_CENTER_POS[duongDuocChon]
        temp = Dynamic_Sprite(img, (road_pos[0], road_pos[1]-150), 'center')
        layer_3.add(temp)
        temp.move(road_pos, 'center', _(60))

        k = 0
        while k < _(60):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    temp_ = Dynamic_Sprite(multiline_surface(
                        'GAME PAUSED', font_size=72, rect_size=(800, 450)), (800, 450), 'center')
                    layer_4.add(temp_)
                    is_Running_ = True
                    while is_Running_:
                        for event_ in pygame.event.get():
                            if event_.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event_.type == pygame.KEYDOWN and event_.key == pygame.K_SPACE:
                                is_Running_ = False

                        screen.blit(background, (0, 0))
                        layer_0.draw(screen)
                        layer_1.draw(screen)
                        layer_3.draw(screen)
                        layer_2.draw(screen)
                        layer_4.draw(screen)
                        pygame.display.flip()
                        clock.tick(60)

                    layer_4.empty()

            screen.blit(background, (0, 0))
            layer_0.draw(screen)
            layer_1.draw(screen)
            layer_3.draw(screen)
            layer_2.draw(screen)
            layer_4.draw(screen)
            layer_3.update()
            pygame.display.flip()
            clock.tick(60*SPEED)
            k += 1

        layer_3.empty()
        background.blit(temp.image, temp.rect.topleft)

    def nhanTaiNguyenTuMap(self, list_TnNhan: numpy.ndarray, p_idx):
        '''
        list_TnNhan: 19 phần tử, mỗi phần tử là một ô theo idx, giá trị là số Tn nhận được từ ô đó
        '''
        for tile_idx in range(19):
            if list_TnNhan[tile_idx] != 0:
                num_rei = list_TnNhan[tile_idx]
                res_idx = BOARD.Tile_order[tile_idx]
                for i in range(num_rei):
                    pos = CONST.TILE_CENTER_POS[tile_idx]
                    temp = Dynamic_Sprite(Image.Res_card[res_idx], (pos[0]+32*(
                        i-(num_rei-1)/2.0), pos[1]+18*(i-(num_rei-1)/2.0)), 'center')
                    layer_3.add(temp)
                    print(p_idx, res_idx)
                    des = SPRITE.Player[p_idx].Res_Cards[res_idx].rect.center
                    temp.move(des, 'center', _(120))

        hold_display(_(120), True)
        layer_3.empty()
        list_res_reci = [0 for i in range(5)]
        for i in range(19):
            if list_TnNhan[i] > 0:
                list_res_reci[BOARD.Tile_order[i]] += list_TnNhan[i]

        list_res_str = []
        for i in range(5):
            if list_res_reci[i] > 0:
                list_res_str.append(f'{RES_NAME[i]}*{list_res_reci[i]}')

        return list_res_reci, list_res_str

    def rollDice(self, dice_1, dice_2):
        # layer_1.remove(SPRITE.Button_roll_dice)
        # dice_1 = random.randrange(1,7)
        # dice_2 = random.randrange(1,7)
        SPRITE.Dices[0].set_image(Image.Dice[dice_1])
        SPRITE.Dices[1].set_image(Image.Dice[dice_2])
        layer_0.add(SPRITE.Dices)
        # total_dice = dice_1 + dice_2
        # return total_dice
    
    def traTaiNguyenBank(self, p_idx, res_idx):
        temp = SPRITE.Player[p_idx].Res_Cards[res_idx].copy()
        des = SPRITE.Bank.Res_Cards[res_idx].rect.center
        temp.move(des, 'center', _(60))
        layer_3.add(temp)
        hold_display(_(60), move=True)
        layer_3.empty()
    
    def Robber_move(self, new_Robber_pos):
        layer_0.remove(SPRITE.Robber)
        des = CONST.TILE_CENTER_POS[new_Robber_pos]
        temp = SPRITE.Robber.copy()
        temp.move(des, temp.align, _(60))
        layer_3.add(temp)
        hold_display(_(60), move=True)
        layer_3.remove(temp)
        SPRITE.Robber.set_pos(des)
        layer_0.add(SPRITE.Robber)
    
    def bankTraTaiNguyen(self, p_idx, res_pick_idx):
        temp = SPRITE.Bank.Res_Cards[res_pick_idx].copy()
        des = SPRITE.Player[p_idx].Res_Cards[res_pick_idx].rect.center
        temp.move(des, 'center', _(60))
        layer_3.add(temp)
        hold_display(_(60), move=True)
        layer_3.empty()
    
    def TnTuNguoiChoiNaySangNguoiNguoiKhac(self, p_reci, p_give, res_idx):
        temp = SPRITE.Player[p_give].Res_Cards[res_idx].copy()
        des = SPRITE.Player[p_reci].Res_Cards[res_idx].rect.center
        layer_3.add(temp)
        temp.move(des, 'center', _(60))
        hold_display(_(60), True)
        layer_3.empty()

ANIMATION = Animation()

###########################################################################

# Đầu game
temp =     [0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 2, 2, 1, 1, 0, 0]
temp_num = [1, 0, 2, 0, 3, 0, 4, 0, 1, 0, 2, 0, 3, 0, 4, 0]

for i in range(16):
    p_idx = temp[i]
    BOARD.main_id = p_idx

    compare_numba_graphic(BOARD, env_state)

    print('$$$ ### *** """ Đến turn của:', list_player_name[p_idx], '""" *** ### $$$')

    # Đổi màu tên người chơi chính
    if i > 0:
        change_player_name_color(temp[i-1], RGB_color.SPRING_GREEN)

    change_player_name_color(p_idx, RGB_color.WHITE)

    set_notification(list_player_name[p_idx]+"'s turn")
    hold_display(_(60), False)

    if temp_num[i] != 0:
        for j in range(temp_num[i]):
            ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
            NlChon_Numba, tf, pf = random_player(env.getAgentState(env_state), [0], [0])

            env.stepEnv(env_state, NlChon_Numba)
            NlChon = NlChon_Numba - 59

            # Animation
            BOARD.Bank.ResBank[NlChon] -= 1
            SPRITE.Bank.Number_ResBank[NlChon].set_value(BOARD.Bank.ResBank[NlChon])

            tempDy = SPRITE.Bank.Res_Cards[NlChon].copy()

            des = SPRITE.Player[p_idx].ResBank[NlChon].rect.center
            tempDy.move(des, 'center', _(60))
            layer_3.add(tempDy)
            hold_display(_(60), True)

            BOARD.Player[p_idx].ResBank[NlChon] += 1
            SPRITE.Player[p_idx].Number_ResBank[NlChon].set_value(BOARD.Player[p_idx].ResBank[NlChon])

            layer_3.empty()
    else:
        set_notification(list_player_name[p_idx]+"is placing settlement")

        list_diemCoTheDat = []

        diemDatNha = datNha(p_idx, list_diemCoTheDat)

        if BOARD.Player[p_idx].Score == 2:
            list_tile_nearest = [
                tile_idx for tile_idx in CONST.POINT_TILE[diemDatNha] if BOARD.Tile_order[tile_idx] != 5]
            list_TnNhan = numpy.full(19, 0)
            list_TnNhan[list_tile_nearest] = 1
            list_res_reci, list_res_str = ANIMATION.nhanTaiNguyenTuMap(
                list_TnNhan, p_idx)
            for res_idx in range(5):
                if list_res_reci[res_idx] > 0:
                    BOARD.Bank.Res_Cards[res_idx] -= list_res_reci[res_idx]
                    BOARD.Player[p_idx].Res_Cards[res_idx] += list_res_reci[res_idx]
                    SPRITE.Bank.Number_Res_Cards[res_idx].set_value(
                        BOARD.Bank.Res_Cards[res_idx])
                    SPRITE.Player[p_idx].Number_Res_Cards[res_idx].set_value(
                        BOARD.Player[p_idx].Res_Cards[res_idx])

            set_notification(
                list_player_name[p_idx] + ' got: ' + str(list_res_str))
            hold_display(_(60), False)

        set_notification(list_player_name[p_idx]+"is placing road")

        # Nhận điểm đặt đường
        list_DuongCoTheDat = CONST.POINT_ROAD[diemDatNha]

        datDuong(p_idx, list_DuongCoTheDat)



def get_bank_dev(env):
    return env[53:58].astype(int)


# Mỗi turn

for i in range(10000):
    layTaiNguyenTuKho = True

    layer_0.remove(SPRITE.Dices)
    layer_1.empty()

    p_idx = i % 4
    BOARD.main_id = p_idx

    print('######################################################## Đến người người chơi id',BOARD.main_id, env_state[230] % 4)
    
    print('$$$ ### *** """ Đến turn của:', list_player_name[p_idx], '""" *** ### $$$')
    change_player_name_color((p_idx-1) % 4, RGB_color.SPRING_GREEN)
    change_player_name_color(p_idx, RGB_color.WHITE)
    set_notification(list_player_name[p_idx]+"'s turn")
    hold_display(_(60), False)

    check_dev = False

    list_action = CHECK.listActionDauMoiTurn(p_idx)

    action = 'Ahihi'

    while action != 'pass_turn':
        layer_1.empty()
        set_notification(list_player_name[p_idx]+"'s turn")

        temp_env = env_state.copy()

        if len(list_action) == 1 and list_action[0] == 'roll_dice' and ((BOARD.Player[BOARD.main_id].Dev_Cards[0:4] == 0).all() or check_dev):
            action = 'roll_dice'
        else:
            compare_numba_graphic(BOARD, env_state)
            ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
            temp_dev_1 = get_bank_dev(env_state)

            action_idx, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
            dict_idx_str = {
                54: 'roll_dice',
                55: 'knight',
                56: 'roadbuilding',
                57: 'yearofplenty',
                58: 'monopoly',
                88: 'pass_turn',
                83: 'build_road',
                84: 'build_settlement',
                85: 'build_city',
                86: 'buy_dev',
                87: 'trade_bank',
                94: 'take_res_from_storage'
            }

            action = dict_idx_str[action_idx] # Dịch sang string tại đây

            env.stepEnv(env_state, action_idx)
        
        print(action)

        if action == 'roll_dice':
            total_dice = int(env_state[228])
            min_dice = None
            if total_dice <= 7:
                min_dice = 1
            else:
                min_dice = total_dice - 6
            
            dice_1 = random.randint(min_dice, min(6, total_dice-1))
            dice_2 = total_dice - dice_1

            ANIMATION.rollDice(dice_1, dice_2)

            hold_display(_(60), False)

            if total_dice == 7:
                list_num_return = CHECK.soLuongTaiNguyenTraDo7(p_idx)

                for j in range(4):
                    if list_num_return[j] > 0:
                        sub_p_idx = (p_idx + j) % 4
                        if j != 0:
                            change_player_name_color(
                                sub_p_idx, RGB_color.BLACK)
                        
                        set_notification(
                            list_player_name[sub_p_idx]+': resources overlimited, must return '+str(list_num_return[j]))
                        hold_display(_(120), False)
                        set_notification(
                            list_player_name[sub_p_idx]+' is choosing resource to return')
                        
                        for k in range(list_num_return[j]):
                            ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
                            res_idx_return_numba, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
                            res_idx_return = res_idx_return_numba - 89 # Dịch sang 0, 1, 2, 3, 4

                            env.stepEnv(env_state, res_idx_return_numba)

                            BOARD.Player[sub_p_idx].Res_Cards[res_idx_return] -= 1
                            SPRITE.Player[sub_p_idx].Number_Res_Cards[res_idx_return].set_value(
                                BOARD.Player[sub_p_idx].Res_Cards[res_idx_return])
                            ANIMATION.traTaiNguyenBank(
                                sub_p_idx, res_idx_return)
                            BOARD.Bank.Res_Cards[res_idx_return] += 1
                            SPRITE.Bank.Number_Res_Cards[res_idx_return].set_value(
                                BOARD.Bank.Res_Cards[res_idx_return])
                        
                        if j != 0:
                            change_player_name_color(
                                sub_p_idx, RGB_color.SPRING_GREEN)
                
                diChuyenRobber(p_idx)
            
            else:  # Trả tài nguyên cho người chơi
                list_p_res_reci = [numpy.full(19, 0) for j in range(4)]
                list_tile_in_dice = [k for k in range(
                    19) if BOARD.Prob_order[k] == total_dice and BOARD.Robber_location != k]

                total_reci = numpy.full(19, 0)
                for j in range(4):
                    sub_p_idx = (p_idx + j) % 4
                    for tile_idx in list_tile_in_dice:
                        for point in CONST.TILE_POINT[tile_idx]:
                            if abs(BOARD.Settlements_and_Cities_state[point]) == sub_p_idx+1:
                                if BOARD.Settlements_and_Cities_state[point] > 0:
                                    list_p_res_reci[j][tile_idx] += 1
                                else:
                                    list_p_res_reci[j][tile_idx] += 2

                    total_reci += list_p_res_reci[j]

                total_res_reci = numpy.full(5, 0)
                for k in range(19):
                    if BOARD.Tile_order[k] != 5:
                        total_res_reci[BOARD.Tile_order[k]] += total_reci[k]

                for res_idx in range(5):
                    if total_res_reci[res_idx] > BOARD.Bank.Res_Cards[res_idx]:
                        for k in range(19):
                            if BOARD.Tile_order[k] == res_idx:
                                for j in range(4):
                                    list_p_res_reci[j][k] = 0

                for j in range(4):
                    sub_p_idx = (p_idx + j) % 4
                    if sum(list_p_res_reci[j]) > 0:
                        list_res_reci, list_res_str = ANIMATION.nhanTaiNguyenTuMap(
                            list_p_res_reci[j], sub_p_idx)
                        for res_idx in range(5):
                            if list_res_reci[res_idx] > 0:
                                BOARD.Bank.Res_Cards[res_idx] -= list_res_reci[res_idx]
                                BOARD.Player[sub_p_idx].Res_Cards[res_idx] += list_res_reci[res_idx]
                                SPRITE.Bank.Number_Res_Cards[res_idx].set_value(
                                    BOARD.Bank.Res_Cards[res_idx])
                                SPRITE.Player[sub_p_idx].Number_Res_Cards[res_idx].set_value(
                                    BOARD.Player[sub_p_idx].Res_Cards[res_idx])

                        set_notification(
                            list_player_name[sub_p_idx] + ' got: ' + str(list_res_str))
                        hold_display(_(60), False)
        
        elif action == 'buy_dev':
            traNhieuTN(p_idx, [2, 3, 4])

            temp_dev_2 = get_bank_dev(env_state)
            temp_dev_3 = temp_dev_1 - temp_dev_2
            dev_idx = np.where(temp_dev_3 == 1)[0][0]
            BOARD.Bank.Dev_Cards[dev_idx] -= 1
            SPRITE.Bank.Number_Dev_Cards.set_value(np.sum(BOARD.Bank.Dev_Cards))

            # Animation
            temp = SPRITE.Bank.Dev_Cards.copy()
            temp.set_image(Image.Dev_card[dev_idx])
            des = SPRITE.Player[p_idx].Dev_Cards[dev_idx].rect.center
            temp.move(des, 'center', _(120))
            layer_3.add(temp)
            hold_display(_(120), move=True)
            layer_3.remove(temp)
            BOARD.Player[p_idx].Dev_Cards[dev_idx] += 1
            SPRITE.Player[p_idx].Number_Dev_Cards[dev_idx].set_value(
                BOARD.Player[p_idx].Dev_Cards[dev_idx])

            if dev_idx == 4:
                SPRITE.Player[p_idx].Score.set_value(
                    f'{BOARD.Player[p_idx].Score} ({BOARD.Player[p_idx].Dev_Cards[4]})')
                check_win()
        
        elif action == 'build_road':
            traNhieuTN(p_idx, [0, 1])
            set_notification(list_player_name[p_idx]+"is placing road")
            list_duongCoTheDat = CHECK.viTriXayDuong(p_idx)[1]
            datDuongGiuaGame(p_idx, list_duongCoTheDat)
            check_longest_Road()
            check_win()

        elif action == 'build_settlement':
            list_diemCoTheDat = CHECK.khaNangXayNha(p_idx)[1]
            traNhieuTN(p_idx, [0, 1, 2, 3])
            set_notification(list_player_name[p_idx]+"is placing settlement")
            datNha(p_idx, list_diemCoTheDat)
            check_longest_Road()
            check_win()

        elif action == 'build_city':
            list_diemCoTheDat = CHECK.khaNangXayThanhPho(p_idx)[1]
            traNhieuTN(p_idx, [3, 3, 4, 4, 4])
            set_notification(list_player_name[p_idx]+"is building city")
            datThanhPho(p_idx, list_diemCoTheDat)
            check_win()

        elif action == 'trade_bank':
            layer_1.empty()
            set_notification(
                list_player_name[p_idx] + ' is choosing resource to GIVE in trade (with bank) (click on your name to go to next step)')
            hold_display(_(60), move=False)

            list_tnCoTheChon = [res_idx for res_idx in range(
                5) if BOARD.Player[p_idx].Res_Cards[res_idx] >= BOARD.Player[p_idx].Card_exchange_rate[res_idx]]
            for res_idx in list_tnCoTheChon:
                check_abcxyz = False
                for res_idx_1 in range(5):
                    if res_idx_1 != res_idx and BOARD.Bank.Res_Cards[res_idx_1] > 0:
                        check_abcxyz = True

                if not check_abcxyz:
                    list_tnCoTheChon.remove(res_idx)

            ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
            res_pick_idx_numba, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
            res_pick_idx = res_pick_idx_numba - 89 # Dịch sang 0,1,2,3,4

            env.stepEnv(env_state, res_pick_idx_numba)

            # print(res_pick_idx)
            for k in range(BOARD.Player[p_idx].Card_exchange_rate[res_pick_idx]):
                BOARD.Player[p_idx].Res_Cards[res_pick_idx] -= 1
                SPRITE.Player[p_idx].Number_Res_Cards[res_pick_idx].set_value(
                    BOARD.Player[p_idx].Res_Cards[res_pick_idx])
                ANIMATION.traTaiNguyenBank(p_idx, res_pick_idx)
                BOARD.Bank.Res_Cards[res_pick_idx] += 1
                SPRITE.Bank.Number_Res_Cards[res_pick_idx].set_value(
                    BOARD.Bank.Res_Cards[res_pick_idx])

            set_notification(
                list_player_name[p_idx] + ' is choosing resource to RECEIVE in trade (with bank) (click on your name to go to next step)')
            hold_display(_(60), move=False)

            list_tnCoTheChon = [res_idx for res_idx in range(
                5) if BOARD.Bank.Res_Cards[res_idx] > 0 and res_idx != res_pick_idx]

            ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
            res_pick_idx_numba, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
            res_pick_idx = res_pick_idx_numba - 59 #Dịch sang 0,1,2,3,4

            env.stepEnv(env_state, res_pick_idx_numba)

            # print(res_pick_idx)
            BOARD.Bank.Res_Cards[res_pick_idx] -= 1
            SPRITE.Bank.Number_Res_Cards[res_pick_idx].set_value(
                BOARD.Bank.Res_Cards[res_pick_idx])
            ANIMATION.bankTraTaiNguyen(p_idx, res_pick_idx)
            BOARD.Player[p_idx].Res_Cards[res_pick_idx] += 1
            SPRITE.Player[p_idx].Number_Res_Cards[res_pick_idx].set_value(
                BOARD.Player[p_idx].Res_Cards[res_pick_idx])
        
        elif action in DEV_NAME:
            check_dev = True
            set_notification(
                list_player_name[p_idx] + ' used devcard: '+str(action))
            hold_display(_(120), move=False)
            BOARD.Player[p_idx].Dev_Cards[DEV_NAME.index(action)] -= 1
            SPRITE.Player[p_idx].Number_Dev_Cards[DEV_NAME.index(action)].set_value(
                BOARD.Player[p_idx].Dev_Cards[DEV_NAME.index(action)])

            if action == 'knight':
                diChuyenRobber(p_idx)
                BOARD.Player[p_idx].Used_Knight_Cards += 1
                SPRITE.Player[p_idx].Amount_used_knight.set_value(
                    BOARD.Player[p_idx].Used_Knight_Cards)
                if BOARD.Player[p_idx].Used_Knight_Cards > 2:
                    check_largest_Army(p_idx)
                    check_win()

            elif action == 'roadbuilding':
                for k in range(2):
                    listDuongCoTheDat = CHECK.viTriXayDuong(p_idx)[1]
                    if len(listDuongCoTheDat) > 0:
                        datDuongGiuaGame(p_idx, listDuongCoTheDat)
                        check_longest_Road()
                        check_win()

            elif action == 'yearofplenty':
                for k in range(2):
                    list_tnCoTheChon = [res_idx for res_idx in range(
                        5) if BOARD.Bank.Res_Cards[res_idx] > 0]
                    if len(list_tnCoTheChon) > 0:
                        ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
                        res_pick_idx_numba, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
                        res_pick_idx = res_pick_idx_numba - 59 #Dịch sang 0,1,2,3,4

                        env.stepEnv(env_state, res_pick_idx_numba)

                        # print(res_pick_idx)

                        BOARD.Bank.Res_Cards[res_pick_idx] -= 1
                        SPRITE.Bank.Number_Res_Cards[res_pick_idx].set_value(
                            BOARD.Bank.Res_Cards[res_pick_idx])
                        ANIMATION.bankTraTaiNguyen(p_idx, res_pick_idx)
                        BOARD.Player[p_idx].Res_Cards[res_pick_idx] += 1
                        SPRITE.Player[p_idx].Number_Res_Cards[res_pick_idx].set_value(
                            BOARD.Player[p_idx].Res_Cards[res_pick_idx])
            
            elif action == 'monopoly':
                ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
                res_pick_idx_numba, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
                res_pick_idx = res_pick_idx_numba - 59 #Dịch sang 0,1,2,3,4


                env.stepEnv(env_state, res_pick_idx_numba)

                # for j in range(1, 4):
                #     sub_p_idx = (p_idx + j) % 4
                #     if BOARD.Player[sub_p_idx].Res_Cards[res_pick_idx] > 0:
                #         for k in range(BOARD.Player[sub_p_idx].Res_Cards[res_pick_idx]):
                #             BOARD.Player[sub_p_idx].Res_Cards[res_pick_idx] -= 1
                #             SPRITE.Player[sub_p_idx].Number_Res_Cards[res_pick_idx].set_value(
                #                 BOARD.Player[sub_p_idx].Res_Cards[res_pick_idx])
                #             ANIMATION.TnTuNguoiChoiNaySangNguoiNguoiKhac(
                #                 p_idx, sub_p_idx, res_pick_idx)
                #             BOARD.Player[p_idx].Res_Cards[res_pick_idx] += 1
                #             SPRITE.Player[p_idx].Number_Res_Cards[res_pick_idx].set_value(
                #                 BOARD.Player[p_idx].Res_Cards[res_pick_idx])

                print('Nguyên liệu lấy khi dùng thẻ nomopoly', res_pick_idx, 'Nguyên liệu bank còn', BOARD.Bank.Res_Cards[res_pick_idx])
                if BOARD.Bank.Res_Cards[res_pick_idx] > 0:
                    so_res_lay = 19 - BOARD.Bank.Res_Cards[res_pick_idx]
                    if so_res_lay > BOARD.Bank.Res_Cards[res_pick_idx]:
                        so_res_lay = BOARD.Bank.Res_Cards[res_pick_idx]
                    print('Số nguyên liệu lấy', so_res_lay, BOARD.Player[p_idx].Res_Cards[res_pick_idx])
                    for k in range(so_res_lay):
                        BOARD.Bank.Res_Cards[res_pick_idx] -= 1
                        SPRITE.Bank.Number_Res_Cards[res_pick_idx].set_value(
                            BOARD.Bank.Res_Cards[res_pick_idx])
                        ANIMATION.bankTraTaiNguyen(p_idx, res_pick_idx)
                        BOARD.Player[p_idx].Res_Cards[res_pick_idx] += 1
                        SPRITE.Player[p_idx].Number_Res_Cards[res_pick_idx].set_value(
                            BOARD.Player[p_idx].Res_Cards[res_pick_idx])
                    print('Số nguyên liệu sau khi lấy', BOARD.Player[p_idx].Res_Cards[res_pick_idx])
                # raise 'Done'
        elif action == 'take_res_from_storage':
            ''' $$$ ### *** """ Nhận action """ *** ### $$$ '''
            res_pick_idx_numba, tf, pf = random_player(env.getAgentState(env_state), [0], [0])
            res_pick_idx = res_pick_idx_numba  - 59 #Dịch sang 0,1,2,3,4

            env.stepEnv(env_state, res_pick_idx_numba)

            BOARD.Player[p_idx].ResBank[res_pick_idx] -= 1
            SPRITE.Player[p_idx].Number_ResBank[res_pick_idx].set_value(BOARD.Player[p_idx].ResBank[res_pick_idx])

            tempDy = SPRITE.Player[p_idx].ResBank[res_pick_idx].copy()

            des = SPRITE.Player[p_idx].Res_Cards[res_pick_idx].rect.center

            tempDy.move(des, 'center', _(60))
            layer_3.add(tempDy)
            hold_display(_(60), True)

            BOARD.Player[p_idx].Res_Cards[res_pick_idx] += 1
            SPRITE.Player[p_idx].Number_Res_Cards[res_pick_idx].set_value(BOARD.Player[p_idx].Res_Cards[res_pick_idx])

            layer_3.empty()

            layTaiNguyenTuKho = False
        
        #########################
        if action == 'roll_dice':
            list_action.remove('roll_dice')
            list_action.append('pass_turn')

            list_action = CHECK.actionCoTheLam(
                p_idx, list_action, layTaiNguyenTuKho)

        elif action in DEV_NAME:
            if 'roll_dice' in list_action:
                list_action = ['roll_dice']
            else:
                for dev_name in DEV_NAME:
                    if dev_name in list_action:
                        list_action.remove(dev_name)

                list_action = CHECK.actionCoTheLam(
                    p_idx, list_action, layTaiNguyenTuKho)
        
        elif action == 'take_res_from_storage':
            list_action.remove('take_res_from_storage')

        else:
            list_action = CHECK.actionCoTheLam(
                p_idx, list_action, layTaiNguyenTuKho)
