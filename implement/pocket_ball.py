import socket
import time
import math

# 닉네임을 사용자에 맞게 변경해 주세요.
NICKNAME = '서울_4반_손준호'

# 일타싸피 프로그램을 로컬에서 실행할 경우 변경하지 않습니다.
HOST = '127.0.0.1'

# 일타싸피 프로그램과 통신할 때 사용하는 코드값으로 변경하지 않습니다.
PORT = 1447
CODE_SEND = 9901
CODE_REQUEST = 9902
SIGNAL_ORDER = 9908
SIGNAL_CLOSE = 9909

# 게임 환경에 대한 상수입니다.
TABLE_WIDTH = 254
TABLE_HEIGHT = 127
NUMBER_OF_BALLS = 6
HOLES = [[0, 0], [127, 0], [254, 0], [0, 127], [127, 127], [254, 127]]

order = 0
balls = [[0, 0] for i in range(NUMBER_OF_BALLS)]

sock = socket.socket()
print('Trying to Connect: %s:%d' % (HOST, PORT))
sock.connect((HOST, PORT))
print('Connected: %s:%d' % (HOST, PORT))

send_data = '%d/%s' % (CODE_SEND, NICKNAME)
sock.send(send_data.encode('utf-8'))
print('Ready to play!\n--------------------')


class Vector:
    """
    present 2D vector
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __abs__(self):
        return math.hypot(self.x, self.y)


def board_degree(w: float, h: float) -> float:
    """
    보드상의 극좌표 각도를 계산합니다.
    (y 축에서부터 시계방향으로 0 ~ 360 deg, 0 ~ pi rad)
    """
    # 목적구가 흰 공과 상하좌우로 일직선상에 위치했을 때 각도 입력
    if w == 0:
        if h > 0:
            return 0
        else:
            return 180
    elif h == 0:
        if w > 0:
            return 90
        else:
            return 270
    else:
        radian = math.atan(w / h)
        if h > 0:
            return math.degrees(radian)
        # 목적구가 흰 공을 중심으로 아래에 위치했을 때 각도를 재계산
        else:
            return 180 + math.degrees(radian)


def hit_ball(pocket: Vector, t_ball: Vector):
    """
    홀과 목적구의 정보로부터 힘, 각도를 반환합니다. (no-cushions)
    """
    tar_d = pocket - t_ball

    target_deg = board_degree(tar_d.x, tar_d.y)
    hit_x = target.x - diameter * math.sin(math.radians(target_deg))
    hit_y = target.y - diameter * math.cos(math.radians(target_deg))
    hit_point = Vector(hit_x, hit_y)

    # width, height: 목적구와 흰 공의 X좌표 간의 거리, Y좌표 간의 거리
    d_wt = hit_point - white

    deg = board_degree(d_wt.x, d_wt.y)

    # distance: 두 점(좌표) 사이의 거리를 계산
    dis = abs(tar_d) + abs(d_wt)

    return deg, dis


while True:

    # Receive Data
    recv_data = (sock.recv(1024)).decode()
    print('Data Received: %s' % recv_data)

    # Read Game Data
    split_data = recv_data.split('/')
    idx = 0

    print(split_data)
    try:
        for i in range(NUMBER_OF_BALLS):
            for j in range(2):
                balls[i][j] = float(split_data[idx])
                idx += 1
    except:
        send_data = '%d/%s' % (CODE_REQUEST, NICKNAME)
        print("Received Data has been currupted, Resend Requested.")
        continue

    # Check Signal for Player Order or Close Connection
    if balls[0][0] == SIGNAL_ORDER:
        order = int(balls[0][1])
        print('\n* You will be the %s player. *\n' % ('first' if order == 1 else 'second'))
        continue
    elif balls[0][0] == SIGNAL_CLOSE:
        break

    # Show Balls' Position
    print('====== Arrays ======')
    for i in range(NUMBER_OF_BALLS):
        print('Ball %d: %f, %f' % (i, balls[i][0], balls[i][1]))
    print('====================')

    angle = 0.0
    distance = 0.0
    power = 0.0

    ##############################
    # 이 위는 일타싸피와 통신하여 데이터를 주고 받기 위해 작성된 부분이므로 수정하면 안됩니다.
    #
    # 모든 수신값은 변수, 배열에서 확인할 수 있습니다.
    #   - order: 1인 경우 선공, 2인 경우 후공을 의미
    #   - balls[][]: 일타싸피 정보를 수신해서 각 공의 좌표를 배열로 저장

    # 여기서부터 코드를 작성하세요.
    # 아래에 있는 것은 샘플로 작성된 코드이므로 자유롭게 변경할 수 있습니다.

    # 공 직경 정보. calibration 으로 실제보다 약간 작게 잡았습니다. (0.03 차이)
    diameter = 5.7
    num = 0
    # 전략 우선도 변수
    priority = -5

    # 선 후공에 따른 target list
    target = list()
    if order == 1:
        target = [1, 3, 5]
    else:
        target = [2, 4, 5]

    for i in range(len(target)):
        if balls[target[i]][1] != -1:
            num = target[i]
            break

    # 흰 공 변수 입력
    white = Vector(*balls[0])

    # target_x, target_y: 목적구의 X, Y좌표를 나타내기 위해 사용한 변수
    target = Vector(*balls[num])
    t_hole = Vector
    min_d = math.hypot(TABLE_WIDTH, TABLE_HEIGHT)

    for hole in HOLES:
        if white.x <= target.x <= hole[0] or hole[0] <= target.x <= white.x:
            way_vector = Vector(*hole) - target
            way_angle = board_degree(way_vector.x, way_vector.y)
            new_theta, new_length = hit_ball(Vector(*hole), target)
            if abs(target.x - hole[0]) + abs(target.y - hole[1]) < max(0, min_d - 15):
                min_d = abs(target.x - hole[0]) + abs(target.y - hole[1])
                t_hole = Vector(*hole)
            elif (max(0, min_d - 15) < abs(target.x - hole[0]) + abs(target.y - hole[1]) < min_d
                and abs(new_theta - way_angle) < math.pi / 6):
                min_d = abs(target.x - hole[0]) + abs(target.y - hole[1])
                t_hole = Vector(*hole)

    angle, distance = hit_ball(t_hole, target)

    # power: 거리 distance 에 따른 힘의 세기를 계산
    # 힘이 너무 약한 경우 공을 쳐서 보낼 수 없기에 최소치를 할당하였습니다.
    power = max(20.0, distance * 0.19)

    # 아래는 일타싸피와 통신하는 나머지 부분이므로 수정하면 안됩니다.
    ##############################

    merged_data = '%f/%f/' % (angle, power)
    sock.send(merged_data.encode('utf-8'))
    print('Data Sent: %s' % merged_data)

sock.close()
print('Connection Closed.\n--------------------')