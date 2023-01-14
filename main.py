import pygame

pygame.init()

screen = pygame.display.set_mode([300, 300])
pygame.display.set_caption('Pong Reboot')

timer = pygame.time.Clock()
framerate = 60
black = (0, 0, 0)
white = (255, 255, 255)
game_over = False
font = pygame.font.SysFont('arial', 27)

player_y = 130
computer_y = 130
ball_x = 145
ball_y = 145
player_direction = 0
player_speed = 5
ball_x_direction = 1
ball_y_direction = 1
ball_speed = 2
ball_y_speed = 2


def update_ai(ball_y, computer_y):
    computer_speed = 3
    if computer_y + 15 > ball_y + 5:
        computer_y -= computer_speed
    elif computer_y + 15 < ball_y + 5:
        computer_y += computer_speed
    return computer_y


def check_collisions(ball, player, computer, ball_x_direction):
    if ball.colliderect(player):
        ball_x_direction = 1
    elif ball.colliderect(computer):
        ball_x_direction = -1

    return ball_x_direction


def update_ball(ball_x_direction, ball_y_direction, ball_x, ball_y, ball_speed, ball_y_speed):
    if ball_x_direction == 1 and ball_x < 290:
        ball_x += ball_speed
    elif ball_x_direction == 1 and ball_x >= 290:
        ball_x_direction *= -1
    if ball_x_direction == -1 and ball_x > 0:
        ball_x -= ball_speed
    elif ball_x_direction == -1 and ball_x <= 0:
        ball_x_direction *= -1

    if ball_y_direction == 1 and ball_y < 290:
        ball_y += ball_y_speed
    elif ball_y_direction == 1 and ball_y >= 290:
        ball_y_direction *= -1
    if ball_y_direction == -1 and ball_y > 0:
        ball_y -= ball_y_speed
    elif ball_y_direction == -1 and ball_y <= 0:
        ball_y_direction *= -1

    return ball_x_direction, ball_y_direction, ball_x, ball_y


def check_game_over(ball_x, game_over):
    if (ball_x <= 0 or ball_x >= 290) and game_over == False:
        game_over = True

    return game_over


running = True
while running:
    timer.tick(framerate)
    screen.fill(black)
    game_over = check_game_over(ball_x, game_over)
    player = pygame.draw.rect(screen, white, [5, player_y, 10, 40])
    computer = pygame.draw.rect(screen, white, [285, computer_y, 10, 40])
    ball = pygame.draw.rect(screen, white, [ball_x, ball_y, 10, 10])
    if not game_over:
        computer_y = update_ai(ball_y, computer_y)
        ball_x_direction, ball_y_direction, ball_x, ball_y = update_ball(ball_x_direction, ball_y_direction, ball_x, ball_y, ball_speed, ball_y_speed)
    ball_x_direction = check_collisions(ball, player, computer, ball_x_direction)

    if game_over:
        game_over_text = font.render('Game Over!', True, white, black)
        screen.blit(game_over_text, (80, 130))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_direction = -1
            if event.key == pygame.K_x:
                player_direction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_direction = 0
            if event.key == pygame.K_x:
                player_direction = 0

    player_y += player_speed * player_direction



    pygame.display.flip()

pygame.quit()
