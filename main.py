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
background_image = pygame.image.load("asset/background.jpeg")
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
clock = pygame.time.Clock()

# 플레이어 설정
player_size = PLAYER_LENGTH
player1_pos = [WIDTH - player_size - 50, HEIGHT - player_size - 10]  # 오른쪽에 위치
player2_pos = [50, HEIGHT - player_size - 10]  # 왼쪽에 위치
player_speed = 10
hit_speed = 30  # hit 상태일 때의 속도 감소
dash_speed = 50  # 대시 상태일 때의 속도
jump_strength = 23  # 점프 최대치를 2배로 증가
fall_speed1 = 0
fall_speed2 = 0
is_jumping1 = False
is_jumping2 = False
dash_active1 = False
dash_active2 = False
dash_timer1 = 0
dash_timer2 = 0

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
ball_speed = [random.randint(-10, 10), -15]  # 초기에는 공이 움직이지 않도록 설정
ball_pos = [WIDTH // 2, 50]  # 초기 공 위치를 화면 중앙에 설정

# 네트 설정
net_width = 10
net_height = 200
net_pos = [WIDTH // 2 - net_width // 2, HEIGHT - net_height]

# 목표 점수 설정
target_score = 15

# 첫 공 위치 변수
first_ball = True

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
    # Convert number to integer directly
    return number

def adjust_ball_direction(player_pos, ball_speed, player_image_state):
    # 충돌 감지 및 처리
    if detect_collision(player_pos, ball_pos):
        p_x, p_y = player_pos
        b_x, b_y = ball_pos
        
        if player_image_state == "hit":
            ball_speed[0] = random.choice([-hit_speed, hit_speed])
            ball_speed[1] = -hit_speed
        elif player_image_state in ["receive", "left_dig", "right_dig"]:
            ball_speed[0] = floor_to_int(ball_speed[0] // 2)
            ball_speed[1] = floor_to_int(ball_speed[1] // 2)
        else:
            if b_x < p_x:
                ball_speed[0] = -floor_to_int(abs(b_x - p_x) // 3)
            elif b_x > p_x:
                ball_speed[0] = floor_to_int(abs(b_x - p_x) // 3) 

            if ball_speed[0] == 0:
                ball_speed[0] = (random.randint(0, 2) - 1)

            ball_abs_speed = abs(ball_speed[1])
            ball_speed[1] = -ball_abs_speed

            if ball_abs_speed < 15:
                ball_speed[1] = -15

def reset_ball(winner_pos):
    global ball_pos, ball_speed, first_ball
    if first_ball:
        ball_pos = [winner_pos[0] + player_size // 2, winner_pos[1] - ball_size]
        first_ball = False
    else:
        ball_pos = [winner_pos[0] + player_size // 2, winner_pos[1] - ball_size]
    ball_speed = [0, 15]  # 공이 처음에는 수직으로 떨어지도록 설정

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
    game_over_active = True
    while game_over_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
                game_over_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH // 2 - 200 < event.pos[0] < WIDTH // 2 and HEIGHT // 2 < event.pos[1] < HEIGHT // 2 + 50:
                    restart_game()
                    game_over_active = False
                if WIDTH // 2 < event.pos[0] < WIDTH // 2 + 200 and HEIGHT // 2 < event.pos[1] < HEIGHT // 2 + 50:
                    quit_game()
                    game_over_active = False

def restart_game():
    global score1, score2, ball_pos, ball_speed, player1_pos, player2_pos, player1_image_state, player2_image_state, is_jumping1, is_jumping2, fall_speed1, fall_speed2, first_ball, dash_active1, dash_active2, dash_timer1, dash_timer2
    score1 = 0
    score2 = 0
    first_ball = True
    dash_active1 = False
    dash_active2 = False
    dash_timer1 = 0
    dash_timer2 = 0
    player1_pos = [WIDTH - player_size - 50, HEIGHT - player_size - 10]
    player2_pos = [50, HEIGHT - player_size - 10]
    reset_ball(player1_pos)
    player1_image_state = "receive"
    player2_image_state = "receive"
    is_jumping1 = False
    is_jumping2 = False
    fall_speed1 = 0
    fall_speed2 = 0
    main_game()

def quit_game():
    global running
    running = False
    pygame.quit()
    exit()

def dash(player_pos, direction):
    if direction == "left":
        player_pos[0] -= dash_speed
    elif direction == "right":
        player_pos[0] += dash_speed

def dash_animation(player_image_state, direction, player_number):
    if direction == "left":
        player_image_state = "left_dig"
    elif direction == "right":
        player_image_state = "right_dig"
    pygame.time.set_timer(pygame.USEREVENT + player_number, 200)  # 0.2초 후에 이벤트 발생
    return player_image_state

def restore_image(player_image_state, player_number):
    if player_number == 1:
        player_image_state = "receive"
    elif player_number == 2:
        player_image_state = "receive"
    return player_image_state

def main_game():
    global running, score1, score2, player1_image_state, player2_image_state, is_jumping1, is_jumping2, fall_speed1, fall_speed2, first_ball, dash_active1, dash_active2, dash_timer1, dash_timer2
    running = True
    
    while running:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.USEREVENT + 1:
                player1_image_state = restore_image(player1_image_state, 1)
                dash_active1 = False
            elif event.type == pygame.USEREVENT + 2:
                player2_image_state = restore_image(player2_image_state, 2)
                dash_active2 = False

        keys = pygame.key.get_pressed()

        # 플레이어 1 이동 및 점프
        current_speed1 = hit_speed if player1_image_state == "hit" else player_speed
        if player1_image_state == "hit":
            current_speed1 = player_speed // 2  # hit 상태에서는 속도가 느려짐
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
        if player2_image_state == "hit":
            current_speed2 = player_speed // 2  # hit 상태에서는 속도가 느려짐
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
                ball_speed[0] = random.choice([-hit_speed, hit_speed])
                ball_speed[1] = -hit_speed

        # 플레이어 1 대시
        if keys[pygame.K_LEFT] and keys[pygame.K_RSHIFT] and not dash_active1:
            dash_active1 = True
            dash(player1_pos, "left")
            player1_image_state = dash_animation(player1_image_state, "left", 1)

        if keys[pygame.K_RIGHT] and keys[pygame.K_RSHIFT] and not dash_active1:
            dash_active1 = True
            dash(player1_pos, "right")
            player1_image_state = dash_animation(player1_image_state, "right", 1)

        # 플레이어 2 대시
        if keys[pygame.K_a] and keys[pygame.K_n] and not dash_active2:
            dash_active2 = True
            dash(player2_pos, "left")
            player2_image_state = dash_animation(player2_image_state, "left", 2)

        if keys[pygame.K_d] and keys[pygame.K_n] and not dash_active2:
            dash_active2 = True
            dash(player2_pos, "right")
            player2_image_state = dash_animation(player2_image_state, "right", 2)

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
                ball_speed[0] = random.choice([-hit_speed, hit_speed])
                ball_speed[1] = -hit_speed

        # 공 이동
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        # 충돌 감지 및 처리
        adjust_ball_direction(player1_pos, ball_speed, player1_image_state)
        adjust_ball_direction(player2_pos, ball_speed, player2_image_state)

        # 공 벽 충돌
        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH - ball_size:
            ball_speed[0] = -ball_speed[0]
        if ball_pos[1] <= 0:
            ball_speed[1] = -ball_speed[1]

        # 공이 네트에 충돌했을 때
        if net_pos[0] <= ball_pos[0] <= net_pos[0] + net_width and net_pos[1] <= ball_pos[1] <= net_pos[1] + net_height:
            ball_speed[0] = -ball_speed[0]

        # 공이 땅에 떨어졌을 때 점수 업데이트
        if ball_pos[1] >= HEIGHT:
            if ball_pos[0] < WIDTH // 2:
                score2 += 1
                reset_ball(player2_pos)
            else:
                score1 += 1
                reset_ball(player1_pos)

            if score1 == target_score:
                game_over(1)
            elif score2 == target_score:
                game_over(2)

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

def main_menu():
    global target_score
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50)
    font = pygame.font.Font(None, 74)
    title_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 50)
    active = False
    input_text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            target_score = int(input_text)
                            main_game()
                        except ValueError:
                            input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        
        # 게임 제목
        title_surface = title_font.render("Active Volley Ball", True, BLUE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_surface, title_rect)

        # 입력 안내 문구
        prompt_surface = font.render("Enter Target Score:", True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        screen.blit(prompt_surface, prompt_rect)

        # 중앙 정렬된 입력 텍스트
        txt_surface = font.render(input_text, True, BLACK)
        txt_rect = txt_surface.get_rect(center=input_box.center)
        screen.blit(txt_surface, txt_rect)
        pygame.draw.rect(screen, BLACK, input_box, 2)

        draw_button("Start", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, GREEN, button_font, lambda: main_game())

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()
    pygame.quit()
    exit()