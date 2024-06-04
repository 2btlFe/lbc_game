import pygame
import random

# 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 화면 크기 설정
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pikachu Volleyball")

# 플레이어 설정
player_size = 50
player1_pos = [50, HEIGHT - player_size - 10]
player2_pos = [WIDTH - player_size - 50, HEIGHT - player_size - 10]
player_speed = 10

# 공 설정
ball_size = 20
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [random.choice([-5, 5]), -5]

# 네트 설정
net_width = 10
net_height = 150
net_pos = [WIDTH // 2 - net_width // 2, HEIGHT - net_height]

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 플레이어 1 이동
    if keys[pygame.K_a]:
        player1_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player1_pos[0] += player_speed
    if keys[pygame.K_w]:
        player1_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player1_pos[1] += player_speed

    # 플레이어 2 이동
    if keys[pygame.K_LEFT]:
        player2_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player2_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player2_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player2_pos[1] += player_speed

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
