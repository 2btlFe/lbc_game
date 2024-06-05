import pygame
import random
import math

# 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 화면 크기 설정
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pikachu Volleyball")

# 플레이어 설정
player_size = 50
player1_pos = [WIDTH - player_size - 50, HEIGHT - player_size - 10]  # 오른쪽에 위치
player2_pos = [50, HEIGHT - player_size - 10]  # 왼쪽에 위치
player_speed = 7
jump_strength = 23  # 점프 최대치를 2배로 증가
fall_speed1 = 0
fall_speed2 = 0
is_jumping1 = False
is_jumping2 = False

# 공 설정
ball_size = 20
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [10, -5]

# 네트 설정
net_width = 10
net_height = 200
net_pos = [WIDTH // 2 - net_width // 2, HEIGHT - net_height]

# 충돌 감지 함수
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

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 플레이어 1 이동 및 점프
    if keys[pygame.K_RIGHT] and player1_pos[0] < WIDTH - player_size:
        player1_pos[0] += player_speed
    if keys[pygame.K_LEFT] and player1_pos[0] > WIDTH / 2:
        player1_pos[0] -= player_speed

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
    if keys[pygame.K_d] and player2_pos[0] < WIDTH / 2 - player_size:
        player2_pos[0] += player_speed
    if keys[pygame.K_a] and player2_pos[0] > 0:
        player2_pos[0] -= player_speed

    if keys[pygame.K_w] and not is_jumping2:
        is_jumping2 = True
        fall_speed2 = -jump_strength

    if is_jumping2:
        player2_pos[1] += fall_speed2
        fall_speed2 += 1  # 중력 적용
        if player2_pos[1] >= HEIGHT - player_size - 10:
            player2_pos[1] = HEIGHT - player_size - 10
            is_jumping2 = False

    # 충돌 감지 및 처리
    if detect_collision(player1_pos, ball_pos) or detect_collision(player2_pos, ball_pos):
        ball_speed[0] *= -1  # 공의 x 속도를 반전시킴

    # 공 이동
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # 공 벽 충돌
    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH - ball_size:
        ball_speed[0] = -ball_speed[0]
    if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - ball_size:
        ball_speed[1] = -ball_speed[1]

    # 화면 그리기
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (*player1_pos, player_size, player_size))
    pygame.draw.rect(screen, BLACK, (*player2_pos, player_size, player_size))
    pygame.draw.rect(screen, BLACK, (*net_pos, net_width, net_height))
    pygame.draw.circle(screen, BLACK, ball_pos, ball_size)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
