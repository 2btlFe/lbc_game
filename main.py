import pygame
import random
import math

# 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 화면 크기 설정
WIDTH = 1100
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Insane Volleyball Game")

# 배경 이미지 로드
background_image = pygame.image.load("asset/images.jpeg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Net 관련 상수
HALF_WIDTH = WIDTH / 2
NET_PILLAR_HALF_WIDTH = 50
NET_PILLAR_TOP_TOP_Y_COORD = 352 
NET_PILLAR_TOP_BOTTOM_Y_COORD = 384
PLAYER_LENGTH = 128
PLAYER_HALF_LENGTH = PLAYER_LENGTH / 2
PLAYER_TOUCHING_GROUND_Y_COORD = 504
BALL_RADIUS = 40

# 점수 초기화
score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)

# 플레이어 설정
player_size = PLAYER_LENGTH
player1_pos = [WIDTH - player_size - 50, HEIGHT - player_size - 10]  # 오른쪽에 위치
player2_pos = [50, HEIGHT - player_size - 10]  # 왼쪽에 위치
player_speed = 10
hit_speed = 2  # hit 상태일 때의 속도
jump_strength = 23  # 점프 최대치를 2배로 증가
fall_speed1 = 0
fall_speed2 = 0
is_jumping1 = False
is_jumping2 = False

# 플레이어 이미지 로드
player1_image = {
    "receive": pygame.transform.scale(pygame.image.load("asset/receive2.png"), (player_size, player_size)),
    "jump": pygame.transform.scale(pygame.image.load("asset/jump2.png"), (player_size, player_size)),
    "spike": pygame.transform.scale(pygame.image.load("asset/spike2.png"), (player_size, player_size)),
    "hit": pygame.transform.scale(pygame.image.load("asset/hit2.png"), (player_size, player_size)),
    "left_dig": pygame.transform.scale(pygame.image.load("asset/dig1.png"), (player_size, player_size)),
    "right_dig": pygame.transform.scale(pygame.image.load("asset/dig2.png"), (player_size, player_size)),
}
player2_image = {
    "receive": pygame.transform.scale(pygame.image.load("asset/receive1.png"), (player_size, player_size)),
    "jump": pygame.transform.scale(pygame.image.load("asset/jump1.png"), (player_size, player_size)),
    "spike": pygame.transform.scale(pygame.image.load("asset/spike1.png"), (player_size, player_size)),
    "hit": pygame.transform.scale(pygame.image.load("asset/hit1.png"), (player_size, player_size)),
    "left_dig": pygame.transform.scale(pygame.image.load("asset/dig1.png"), (player_size, player_size)),
    "right_dig": pygame.transform.scale(pygame.image.load("asset/dig2.png"), (player_size, player_size)),
}

player1_image_state = "receive"
player2_image_state = "receive"

# 공 설정
ball_size = 20
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [15, -15]

# 네트 설정
net_width = 10
net_height = 200
net_pos = [WIDTH // 2 - net_width // 2, HEIGHT - net_height]

# 충돌 감지 및 처리 함수
def detect_collision(player_pos, ball_pos):
    p_x, p_y = player_pos
    b_x, b_y = ball_pos

    # 플레이어와 공 사이의 거리 계산
    distance = math.sqrt((p_x - b_x) ** 2 + (p_y - b_y) ** 2)

    # 플레이어와 공이 충돌했는지 확인
    if distance < (player_size + ball_size) / 2:
        return True
    else:
        return False

def floor_to_int(number):
    # Convert number to its binary representation
    binary_str = bin(math.floor(number))

    # Remove the '0b' prefix and convert binary string to integer
    integer_part = int(binary_str[2:], 2)

    return integer_part

def adjust_ball_direction(player_pos, ball_speed):
    # 충돌 감지 및 처리
    if detect_collision(player_pos, ball_pos):
        p_x, p_y = player_pos
        b_x, b_y = ball_pos
        
        if b_x < p_x:
            ball_speed[0] = -floor_to_int(abs(b_x - p_x) / 3)
        elif b_x > p_x:
            ball_speed[0] = floor_to_int(abs(b_x - p_x) / 3) 

        if ball_speed[0] == 0:
            ball_speed[0] = (random.randint(0, 2) - 1)

        ball_abs_speed = abs(ball_speed[1])
        ball_speed[1] = -ball_abs_speed

        if ball_abs_speed < 15:
            ball_speed[1] = -15

def reset_ball():
    global ball_pos, ball_speed
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_speed = [random.choice([-15, 15]), random.choice([-15, 15])]

def draw_button(text, x, y, width, height, color, font, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

def game_over(winner):
    global running
    screen.fill(WHITE)
    game_over_font = pygame.font.Font(None, 74)
    text = f"Player {winner} wins!"
    text_surf = game_over_font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_surf, text_rect)
    button_font = pygame.font.Font(None, 50)
    draw_button("Restart", WIDTH // 2 - 200, HEIGHT // 2, 200, 50, GREEN, button_font, restart_game)
    draw_button("Quit", WIDTH // 2, HEIGHT // 2, 200, 50, RED, button_font, quit_game)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def restart_game():
    global score1, score2, ball_pos, ball_speed, player1_pos, player2_pos, player1_image_state, player2_image_state
    score1 = 0
    score2 = 0
    reset_ball()
    player1_pos = [WIDTH - player_size - 50, HEIGHT - player_size - 10]
    player2_pos = [50, HEIGHT - player_size - 10]
    player1_image_state = "receive"
    player2_image_state = "receive"

def quit_game():
    global running
    running = False

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 플레이어 1 이동 및 점프
    current_speed1 = hit_speed if player1_image_state == "hit" else player_speed
    if keys[pygame.K_RIGHT] and player1_pos[0] < WIDTH - player_size:
        player1_pos[0] += current_speed1
    if keys[pygame.K_LEFT] and player1_pos[0] > WIDTH / 2:
        player1_pos[0] -= current_speed1

    if keys[pygame.K_UP] and not is_jumping1:
        is_jumping1 = True
        fall_speed1 = -jump_strength

    if is_jumping1:
        player1_pos[1] += fall_speed1
        fall_speed1 += 1  # 중력 적용
        if player1_pos[1] >= HEIGHT - player_size - 10:
            player1_pos[1] = HEIGHT - player_size - 10
            is_jumping1 = False

    # 플레이어 2 이동 및 점프
    current_speed2 = hit_speed if player2_image_state == "hit" else player_speed
    if keys[pygame.K_d] and player2_pos[0] < WIDTH / 2 - player_size:
        player2_pos[0] += current_speed2
    if keys[pygame.K_a] and player2_pos[0] > 0:
        player2_pos[0] -= current_speed2

    if keys[pygame.K_w] and not is_jumping2:
        is_jumping2 = True
        fall_speed2 = -jump_strength

    if is_jumping2:
        player2_pos[1] += fall_speed2
        fall_speed2 += 1  # 중력 적용
        if player2_pos[1] >= HEIGHT - player_size - 10:
            player2_pos[1] = HEIGHT - player_size - 10
            is_jumping2 = False

    # 플레이어 2 이미지 변경
    if is_jumping2:
        player2_image_state = "jump"
    elif detect_collision(player2_pos, ball_pos):
        player2_image_state = "spike"
    else:
        player2_image_state = "receive"

    if keys[pygame.K_b]:
        player2_image_state = "hit"
        if detect_collision(player2_pos, ball_pos):
            ball_speed[0] = random.choice([-30, 30])
            ball_speed[1] = -30
    
    # 플레이어 1 이미지 변경
    if is_jumping1:
        player1_image_state = "jump"
    elif detect_collision(player1_pos, ball_pos):
        player1_image_state = "spike"
    else:
        player1_image_state = "receive"
    if keys[pygame.K_RETURN]:
        player1_image_state = "hit"
        if detect_collision(player1_pos, ball_pos):
            ball_speed[0] = random.choice([-30, 30])
            ball_speed[1] = -30

    # 공 이동
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # 충돌 감지 및 처리
    adjust_ball_direction(player1_pos, ball_speed)
    adjust_ball_direction(player2_pos, ball_speed)

    # 공 벽 충돌
    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH - ball_size:
        ball_speed[0] = -ball_speed[0]
    if ball_pos[1] <= 0:
        ball_speed[1] = -ball_speed[1]

    # 공이 땅에 떨어졌을 때 점수 업데이트
    if ball_pos[1] >= HEIGHT - ball_size:
        if ball_pos[0] < WIDTH // 2:
            score2 += 1
        else:
            score1 += 1

        if score1 == 2:
            game_over(1)
        elif score2 == 2:
            game_over(2)

        reset_ball()

    # 화면 그리기
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    screen.blit(player1_image[player1_image_state], (player1_pos[0], player1_pos[1]))
    screen.blit(player2_image[player2_image_state], (player2_pos[0], player2_pos[1]))
    pygame.draw.rect(screen, BLACK, (*net_pos, net_width, net_height))
    pygame.draw.circle(screen, BLACK, ball_pos, ball_size)

    # 점수 표시
    score_text1 = font.render(f"{score1}", True, RED)
    score_text2 = font.render(f"{score2}", True, BLUE)
    
    screen.blit(score_text1, (100, 20))
    screen.blit(score_text2, (WIDTH - 100, 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
