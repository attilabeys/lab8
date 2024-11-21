import pygame 
import random
import os
pygame.init()

os.chdir('polaroid')

W, H = 1200, 800
FPS = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
bg = (0, 0, 0)

paddleW = 150
paddleH = 25
paddleSpeed = 20
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)
change = 15

ballRadius = 20
ballSpeed = 6
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1

game_score = 0
game_score_fonts = pygame.font.SysFont('comicsansms', 40)
game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (0, 0, 0))
game_score_rect = game_score_text.get_rect()
game_score_rect.center = (210, 20)

collision_sound = pygame.mixer.Sound('catch.mp3')
unbreak_sound = pygame.mixer.Sound('unbreak.mp3')

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    if delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

unbreakable_brick_chance = 0.2 # unbreakable bricks will also be random
perk_brick_chance = 0.1 #perk brick is random
block_list = [pygame.Rect(10 + 120 * i, 50 + 70 * j,
        100, 50) for i in range(10) for j in range (4)]
color_list = [(random.randrange(0, 255), 
    random.randrange(0, 255),  random.randrange(0, 255))
              for i in range(10) for j in range(4)]
for i in range(len(block_list)):
    if random.random() < unbreakable_brick_chance:
        color_list[i] = (0, 255, 0)  # Change color for unbreakable bricks (optional)
for i in range(len(block_list)):
    if random.random() < perk_brick_chance:
        color_list[i] = (255, 255, 0)  # Change color for unbreakable bricks (optional)

losefont = pygame.font.SysFont('comicsansms', 40)
losetext = losefont.render('Game Over', True, (255, 255, 255))
losetextRect = losetext.get_rect()
losetextRect.center = (W // 2, H // 2)

winfont = pygame.font.SysFont('comicsansms', 40)
wintext = losefont.render('You win yay', True, (0, 0, 0))
wintextRect = wintext.get_rect()
wintextRect.center = (W // 2, H // 2)

count = 0


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(bg)
    
    [pygame.draw.rect(screen, color_list[color], block)
     for color, block in enumerate (block_list)] #drawing blocks
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), paddle)
    pygame.draw.circle(screen, pygame.Color(255, 0, 0), ball.center, ballRadius)
    # print(next(enumerate (block_list)))

    ball.x += ballSpeed * dx
    ball.y += ballSpeed * dy

    if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
        dx = -dx

    if ball.centery < ballRadius + 50: 
        dy = -dy
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
        
    hitIndex = ball.collidelist(block_list)

    if hitIndex != -1:
        if color_list[hitIndex] != (0, 255, 0) and color_list[hitIndex] != (255, 255, 0):  # Not an unbreakable brick or perk
            hitColor = color_list.pop(hitIndex)
            hitRect = block_list.pop(hitIndex)
            collision_sound.play()
            game_score += 1
            count += 1
        elif color_list[hitIndex] == (0, 255, 0):
            hitRect = block_list[hitIndex]
            unbreak_sound.play()
        elif color_list[hitIndex] == (255, 255, 0):
            hitColor = color_list.pop(hitIndex)
            hitRect = block_list.pop(hitIndex)
            paddle = pygame.Rect(W // 2 - paddleW // 2 + change, H - paddleH - 30, paddleW + change, paddleH) # size of paddle increased with this perk...
            collision_sound.play()
            
        dx, dy = detect_collision(dx, dy, ball, hitRect)

    if count == 4:
        ballSpeed += 1
        count = 0
        paddle = pygame.Rect(W // 2 - paddleW // 2 - change, H - paddleH - 30, paddleW - change, paddleH)
        change += 5
        
    game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (255, 255, 255))
    screen.blit(game_score_text, game_score_rect)
    
    if ball.bottom > H:
        screen.fill((0, 0, 0))
        screen.blit(losetext, losetextRect)
    elif not len(block_list):
        screen.fill((255,255, 255))
        screen.blit(wintext, wintextRect)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddleSpeed
    if key[pygame.K_RIGHT] and paddle.right < W:
        paddle.right += paddleSpeed

    pygame.display.flip()
    clock.tick(FPS)
