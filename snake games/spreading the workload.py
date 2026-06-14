import pygame
import random

pygame.init()
pygame.display.set_caption("our xelnoblade chronicles at home")

scrn = (800, 600)
surface = pygame.display.set_mode(scrn)

velocity_y = 0
hp = 100
hurt_until = 0

sprdir = "left"

clock = pygame.time.Clock()


def img_load(hurtbool):
    global char_img
    global enemy_img

    if hurtbool:
        char_img = pygame.image.load("char_hurt.png")
    else:
        char_img = pygame.image.load("char.png")

    char_img = pygame.transform.scale(char_img, (64, 64))

    if sprdir == "right":
        char_img = pygame.transform.flip(char_img, True, False)

    enemy_img = pygame.image.load("enemy.png")
    enemy_img = pygame.transform.scale(enemy_img, (64, 64))


img_load(False)

player_rect = pygame.Rect(50, 50, 64, 64)
wall_rect = pygame.Rect(700, 500, 50, 100)
enemy_rect = pygame.Rect(800, 600, 64, 64)

gravity = 0.3

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_rect.x -= 8
        sprdir = "left"

    if keys[pygame.K_RIGHT]:
        player_rect.x += 8
        sprdir = "right"

    if keys[pygame.K_UP]:
        player_rect.y -= 8

    if keys[pygame.K_SPACE]:
        player_rect.y -= 8

    player_rect.clamp_ip(surface.get_rect()) # AI
    enemy_rect.clamp_ip(surface.get_rect())

    # Wall bounce
    if player_rect.colliderect(wall_rect):
        velocity_y = -9

    # Enemy follows player
    if player_rect.x < enemy_rect.x:
        enemy_rect.x -= 4

    if player_rect.x > enemy_rect.x:
        enemy_rect.x += 4

    # Damage + hurt texture timer AI
    current_time = pygame.time.get_ticks()

    if enemy_rect.colliderect(player_rect) and current_time >= hurt_until:
        hp -= 10
        print("HP:", hp)

        hurt_until = current_time + 1500

    # Gravity AI
    velocity_y += gravity
    player_rect.y += velocity_y

    # Choose sprite AI
    if current_time < hurt_until:
        img_load(True)
    else:
        img_load(False)

    # Draw
    surface.fill((100, 216, 230))

    pygame.draw.rect(surface, (255, 0, 0), wall_rect)

    surface.blit(char_img, player_rect)
    surface.blit(enemy_img, enemy_rect)

    # Ground collision AI
    if player_rect.bottom >= scrn[1]:
        player_rect.bottom = scrn[1]
        velocity_y = 0

    clock.tick(100)
    pygame.display.flip()

pygame.quit()